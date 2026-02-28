# MongoDB Collection Design - Ecommerce Sales

## Database and Collection

- **Database**: `ecommerce_sales`
- **Collection**: `orders`

## Document Structure

Embedded approach for read-heavy time-series queries. Each document represents one order.

```json
{
  "_id": ObjectId("..."),
  "order_date": ISODate("2022-11-27T00:00:00Z"),
  "product": {
    "name": "Mouse",
    "category": "Accessories"
  },
  "region": "East",
  "quantity": 7,
  "sales": 1197.00,
  "profit": 106.53
}
```

## Field Descriptions

| Field        | Type     | Description                          |
| ------------ | -------- | ------------------------------------ |
| _id          | ObjectId | Auto-generated document identifier   |
| order_date   | Date     | Order timestamp (ISO 8601)           |
| product      | Object   | Embedded product info                |
| product.name | String   | Product name                         |
| product.category | String | Product category                     |
| region       | String   | Sales region (North, East, South, West) |
| quantity     | Integer  | Units sold                            |
| sales        | Number   | Total sales amount                    |
| profit       | Number   | Profit amount                         |

## Indexes

| Index | Keys | Purpose |
| ----- | ---- | ------- |
| order_date | `{ order_date: 1 }` | Time-series queries, latest record, date range |
| compound | `{ order_date: 1, "product.category": 1 }` | Date range + category filters |

## Design Rationale

- **Embedded product**: Avoids joins; product name and category are denormalized for fast reads.
- **Flat region**: Single string; only 4 values, no need for separate collection.
- **order_date as Date**: Enables range queries and sorting for time-series use cases.
