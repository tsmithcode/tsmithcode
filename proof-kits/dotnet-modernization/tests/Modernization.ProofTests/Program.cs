using System.Text.Json;
using TSmithCode.Modernization.Core;
using TSmithCode.Modernization.Legacy;

var tests = new List<(string Name, Action Execute)>
{
    ("legacy characterization preserves gold priority total", LegacyCharacterization),
    ("modern policy preserves legacy pricing parity", ModernParity),
    ("idempotency prevents duplicate order and outbox writes", IdempotencyBoundary),
    ("invalid order returns explicit field errors", ValidationBoundary),
    ("repository exposes one traceable outbox receipt", OutboxReceipt),
};

var results = new List<object>();
var failures = 0;
foreach (var test in tests)
{
    try
    {
        test.Execute();
        Console.WriteLine($"PASS {test.Name}");
        results.Add(new { test.Name, status = "PASS" });
    }
    catch (Exception exception)
    {
        failures++;
        Console.Error.WriteLine($"FAIL {test.Name}: {exception.Message}");
        results.Add(new { test.Name, status = "FAIL", error = exception.Message });
    }
}

var reports = Path.Combine(Directory.GetCurrentDirectory(), "reports");
Directory.CreateDirectory(reports);
var receipt = new
{
    generatedAtUtc = DateTimeOffset.UtcNow,
    total = tests.Count,
    passed = tests.Count - failures,
    failed = failures,
    results,
};
File.WriteAllText(
    Path.Combine(reports, "test-receipt.json"),
    JsonSerializer.Serialize(receipt, new JsonSerializerOptions { WriteIndented = true }));
File.WriteAllText(
    Path.Combine(reports, "test-receipt.md"),
    $"# Test receipt\n\n- Total: {tests.Count}\n- Passed: {tests.Count - failures}\n- Failed: {failures}\n");

return failures == 0 ? 0 : 1;

static void LegacyCharacterization()
{
    var result = new LegacyOrderProcessor().Process(new("C-100", 10, 100m, "Gold", true));
    Assert.True(result.Accepted, "Legacy order should be accepted.");
    Assert.Equal(989.75m, result.Total, "Legacy total changed unexpectedly.");
}

static void ModernParity()
{
    var command = new CreateOrderCommand("C-100", 10, 100m, "Gold", true);
    var modern = OrderPricingPolicy.Calculate(command);
    var legacy = new LegacyOrderProcessor().Process(new("C-100", 10, 100m, "Gold", true));
    Assert.Equal(legacy.Total, modern.Total, "Modern pricing must preserve characterized behavior.");
}

static void IdempotencyBoundary()
{
    var repository = new InMemoryOrderRepository();
    var service = new OrderApplicationService(repository, new FixedClock());
    var command = new CreateOrderCommand("C-200", 4, 250m, "Silver", false);
    var first = service.Create("ORDER-200", command);
    var second = service.Create("ORDER-200", command);
    Assert.True(first.Succeeded, "First request should succeed.");
    Assert.True(second.WasDuplicate, "Second request should be marked duplicate.");
    Assert.Equal(first.OrderId, second.OrderId, "Duplicate should return the original order.");
    Assert.Equal(1, repository.Orders.Count, "Only one order may be persisted.");
    Assert.Equal(1, repository.Outbox.Count, "Only one outbox event may be persisted.");
}

static void ValidationBoundary()
{
    var service = new OrderApplicationService(new InMemoryOrderRepository(), new FixedClock());
    var result = service.Create(string.Empty, new CreateOrderCommand(string.Empty, 0, 0m, "Standard", false));
    Assert.True(!result.Succeeded, "Invalid request must fail.");
    Assert.Equal(4, result.Errors.Count, "All actionable validation issues should be returned.");
}

static void OutboxReceipt()
{
    var repository = new InMemoryOrderRepository();
    var service = new OrderApplicationService(repository, new FixedClock());
    var receipt = service.Create("ORDER-300", new CreateOrderCommand("C-300", 2, 500m, "Standard", true));
    var message = repository.Outbox.Single();
    Assert.Equal(receipt.OrderId, message.OrderId, "Outbox event must trace to the created order.");
    Assert.Equal("order.accepted.v1", message.EventType, "Event contract changed unexpectedly.");
}

file sealed class FixedClock : IClock
{
    public DateTimeOffset UtcNow => new(2026, 7, 10, 12, 0, 0, TimeSpan.Zero);
}

file static class Assert
{
    public static void True(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
    }

    public static void Equal<T>(T expected, T actual, string message)
        where T : notnull
    {
        if (!EqualityComparer<T>.Default.Equals(expected, actual))
        {
            throw new InvalidOperationException($"{message} Expected={expected}; Actual={actual}");
        }
    }
}
