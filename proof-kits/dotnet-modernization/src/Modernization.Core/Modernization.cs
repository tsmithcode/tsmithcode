using System.Collections.Concurrent;

namespace TSmithCode.Modernization.Core;

public sealed record CreateOrderCommand(
    string CustomerId,
    int Quantity,
    decimal UnitPrice,
    string CustomerTier,
    bool Priority);

public sealed record ValidationIssue(string Field, string Code, string Message);

public sealed record OrderRecord(
    Guid OrderId,
    string IdempotencyKey,
    string CustomerId,
    int Quantity,
    decimal UnitPrice,
    string CustomerTier,
    bool Priority,
    decimal Subtotal,
    decimal Discount,
    decimal PriorityFee,
    decimal Tax,
    decimal Total,
    DateTimeOffset CreatedAt);

public sealed record OutboxMessage(
    Guid MessageId,
    Guid OrderId,
    string EventType,
    string Payload,
    DateTimeOffset CreatedAt);

public sealed record OrderReceipt(
    Guid OrderId,
    string IdempotencyKey,
    decimal Total,
    bool WasDuplicate,
    DateTimeOffset CreatedAt,
    IReadOnlyList<ValidationIssue> Errors)
{
    public bool Succeeded => Errors.Count == 0;
}

public interface IClock
{
    DateTimeOffset UtcNow { get; }
}

public sealed class SystemClock : IClock
{
    public DateTimeOffset UtcNow => DateTimeOffset.UtcNow;
}

public interface IOrderRepository
{
    OrderRecord? FindByIdempotencyKey(string idempotencyKey);
    OrderRecord? FindById(Guid orderId);
    void Save(OrderRecord order, OutboxMessage message);
    IReadOnlyCollection<OrderRecord> Orders { get; }
    IReadOnlyCollection<OutboxMessage> Outbox { get; }
}

public sealed class InMemoryOrderRepository : IOrderRepository
{
    private readonly ConcurrentDictionary<Guid, OrderRecord> _orders = new();
    private readonly ConcurrentDictionary<string, Guid> _idempotency = new(StringComparer.Ordinal);
    private readonly ConcurrentDictionary<Guid, OutboxMessage> _outbox = new();
    private readonly object _gate = new();

    public IReadOnlyCollection<OrderRecord> Orders => _orders.Values.ToArray();
    public IReadOnlyCollection<OutboxMessage> Outbox => _outbox.Values.ToArray();

    public OrderRecord? FindByIdempotencyKey(string idempotencyKey)
    {
        return _idempotency.TryGetValue(idempotencyKey, out var orderId)
            && _orders.TryGetValue(orderId, out var order)
                ? order
                : null;
    }

    public OrderRecord? FindById(Guid orderId) =>
        _orders.TryGetValue(orderId, out var order) ? order : null;

    public void Save(OrderRecord order, OutboxMessage message)
    {
        lock (_gate)
        {
            if (_idempotency.ContainsKey(order.IdempotencyKey))
            {
                return;
            }

            _orders[order.OrderId] = order;
            _idempotency[order.IdempotencyKey] = order.OrderId;
            _outbox[message.MessageId] = message;
        }
    }
}

public static class OrderPricingPolicy
{
    public static (decimal Subtotal, decimal Discount, decimal PriorityFee, decimal Tax, decimal Total) Calculate(
        CreateOrderCommand command)
    {
        var subtotal = command.Quantity * command.UnitPrice;
        var discountRate = command.CustomerTier.Trim().ToUpperInvariant() switch
        {
            "GOLD" => 0.10m,
            "SILVER" => 0.05m,
            _ => 0m,
        };
        var discount = decimal.Round(subtotal * discountRate, 2, MidpointRounding.AwayFromZero);
        var priorityFee = command.Priority ? 25m : 0m;
        var taxable = subtotal - discount + priorityFee;
        var tax = decimal.Round(taxable * 0.07m, 2, MidpointRounding.AwayFromZero);
        return (subtotal, discount, priorityFee, tax, taxable + tax);
    }
}

public sealed class OrderApplicationService(IOrderRepository repository, IClock clock)
{
    public OrderReceipt Create(string idempotencyKey, CreateOrderCommand command)
    {
        var normalizedKey = idempotencyKey.Trim();
        var errors = Validate(normalizedKey, command);
        if (errors.Count > 0)
        {
            return new(Guid.Empty, normalizedKey, 0m, false, clock.UtcNow, errors);
        }

        var existing = repository.FindByIdempotencyKey(normalizedKey);
        if (existing is not null)
        {
            return new(existing.OrderId, existing.IdempotencyKey, existing.Total, true, existing.CreatedAt, []);
        }

        var pricing = OrderPricingPolicy.Calculate(command);
        var order = new OrderRecord(
            Guid.NewGuid(),
            normalizedKey,
            command.CustomerId.Trim(),
            command.Quantity,
            command.UnitPrice,
            command.CustomerTier.Trim(),
            command.Priority,
            pricing.Subtotal,
            pricing.Discount,
            pricing.PriorityFee,
            pricing.Tax,
            pricing.Total,
            clock.UtcNow);
        var message = new OutboxMessage(
            Guid.NewGuid(),
            order.OrderId,
            "order.accepted.v1",
            $"{{\"orderId\":\"{order.OrderId}\",\"total\":{order.Total:0.00}}}",
            order.CreatedAt);

        repository.Save(order, message);
        var persisted = repository.FindByIdempotencyKey(normalizedKey) ?? order;
        var wasDuplicate = persisted.OrderId != order.OrderId;
        return new(persisted.OrderId, persisted.IdempotencyKey, persisted.Total, wasDuplicate, persisted.CreatedAt, []);
    }

    private static IReadOnlyList<ValidationIssue> Validate(string idempotencyKey, CreateOrderCommand command)
    {
        var issues = new List<ValidationIssue>();
        if (string.IsNullOrWhiteSpace(idempotencyKey))
        {
            issues.Add(new("Idempotency-Key", "required", "A stable idempotency key is required."));
        }
        if (string.IsNullOrWhiteSpace(command.CustomerId))
        {
            issues.Add(new(nameof(command.CustomerId), "required", "CustomerId is required."));
        }
        if (command.Quantity <= 0)
        {
            issues.Add(new(nameof(command.Quantity), "positive", "Quantity must be greater than zero."));
        }
        if (command.UnitPrice <= 0m)
        {
            issues.Add(new(nameof(command.UnitPrice), "positive", "UnitPrice must be greater than zero."));
        }
        return issues;
    }
}
