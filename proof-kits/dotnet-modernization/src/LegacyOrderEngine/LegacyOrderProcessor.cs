namespace TSmithCode.Modernization.Legacy;

public sealed record LegacyOrderRequest(
    string CustomerId,
    int Quantity,
    decimal UnitPrice,
    string CustomerTier,
    bool Priority);

public sealed record LegacyOrderResult(
    bool Accepted,
    string Status,
    decimal Subtotal,
    decimal Discount,
    decimal PriorityFee,
    decimal Tax,
    decimal Total);

/// <summary>
/// Runnable surrogate for a typical .NET Framework-era service class. The coupled
/// validation, pricing, and status behavior is intentional so characterization tests
/// can protect parity before extraction. It contains no client code.
/// </summary>
public sealed class LegacyOrderProcessor
{
    public LegacyOrderResult Process(LegacyOrderRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.CustomerId))
        {
            return new(false, "CUSTOMER_REQUIRED", 0m, 0m, 0m, 0m, 0m);
        }

        if (request.Quantity <= 0 || request.UnitPrice <= 0m)
        {
            return new(false, "INVALID_LINE", 0m, 0m, 0m, 0m, 0m);
        }

        var subtotal = request.Quantity * request.UnitPrice;
        var discountRate = request.CustomerTier.Trim().ToUpperInvariant() switch
        {
            "GOLD" => 0.10m,
            "SILVER" => 0.05m,
            _ => 0m,
        };
        var discount = decimal.Round(subtotal * discountRate, 2, MidpointRounding.AwayFromZero);
        var priorityFee = request.Priority ? 25m : 0m;
        var taxable = subtotal - discount + priorityFee;
        var tax = decimal.Round(taxable * 0.07m, 2, MidpointRounding.AwayFromZero);
        var total = taxable + tax;

        return new(true, "APPROVED", subtotal, discount, priorityFee, tax, total);
    }
}
