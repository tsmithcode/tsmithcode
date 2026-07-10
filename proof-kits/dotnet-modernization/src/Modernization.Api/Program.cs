using TSmithCode.Modernization.Core;

var builder = WebApplication.CreateBuilder(args);
builder.Logging.ClearProviders();
builder.Logging.AddJsonConsole(options => options.IncludeScopes = true);
builder.Services.AddSingleton<IOrderRepository, InMemoryOrderRepository>();
builder.Services.AddSingleton<IClock, SystemClock>();
builder.Services.AddSingleton<OrderApplicationService>();

var app = builder.Build();

app.Use(async (context, next) =>
{
    var correlationId = context.Request.Headers["X-Correlation-ID"].FirstOrDefault();
    if (string.IsNullOrWhiteSpace(correlationId))
    {
        correlationId = Guid.NewGuid().ToString("N");
    }

    context.Response.Headers["X-Correlation-ID"] = correlationId;
    var logger = context.RequestServices.GetRequiredService<ILoggerFactory>().CreateLogger("Correlation");
    using (logger.BeginScope(new Dictionary<string, object?> { ["CorrelationId"] = correlationId }))
    {
        await next();
    }
});

app.MapGet("/health", (IClock clock) => Results.Ok(new
{
    status = "healthy",
    service = "tsmithcode-dotnet-modernization-proof",
    utc = clock.UtcNow,
}));

app.MapPost("/api/v1/orders", (
    HttpRequest request,
    CreateOrderCommand command,
    OrderApplicationService service) =>
{
    var idempotencyKey = request.Headers["Idempotency-Key"].FirstOrDefault() ?? string.Empty;
    var receipt = service.Create(idempotencyKey, command);
    if (!receipt.Succeeded)
    {
        return Results.Problem(
            statusCode: StatusCodes.Status422UnprocessableEntity,
            title: "Order validation failed",
            detail: "Correct the listed fields and retry with the same idempotency key.",
            extensions: new Dictionary<string, object?> { ["errors"] = receipt.Errors });
    }

    return receipt.WasDuplicate
        ? Results.Ok(receipt)
        : Results.Created($"/api/v1/orders/{receipt.OrderId}", receipt);
});

app.MapGet("/api/v1/orders/{orderId:guid}", (Guid orderId, IOrderRepository repository) =>
{
    var order = repository.FindById(orderId);
    return order is null ? Results.NotFound() : Results.Ok(order);
});

app.MapGet("/api/v1/outbox", (IOrderRepository repository) => Results.Ok(repository.Outbox));

app.Run();
