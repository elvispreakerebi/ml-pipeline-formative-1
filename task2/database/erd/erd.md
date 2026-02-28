# Entity Relationship Diagram - Ecommerce Sales Database

## Mermaid ERD

```mermaid
erDiagram
    categories ||--o{ products : "has"
    products ||--o{ orders : "in"
    regions ||--o{ orders : "in"
    
    categories {
        int category_id PK
        varchar category_name
    }
    
    products {
        int product_id PK
        varchar product_name
        int category_id FK
    }
    
    regions {
        int region_id PK
        varchar region_name
    }
    
    orders {
        int order_id PK
        date order_date
        int product_id FK
        int region_id FK
        int quantity
        decimal sales
        decimal profit
    }
```

## Table Descriptions

| Table       | Role        | Description                                              |
| ----------- | ----------- | -------------------------------------------------------- |
| categories  | Dimension   | Product categories (Office, Accessories, Electronics)    |
| products    | Dimension   | Products with category reference                         |
| regions     | Dimension   | Sales regions (North, East, South, West)                 |
| orders      | Fact        | Time-series order records (date, product, region, metrics)|

## Relationships

- **categories → products**: One-to-many. Each category has many products.
- **products → orders**: One-to-many. Each product appears in many orders.
- **regions → orders**: One-to-many. Each region has many orders.
