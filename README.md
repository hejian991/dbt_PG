# DBT PostgreSQL Project

This is a dbt project configured to work with PostgreSQL database.

## Project Structure

This project contains:
- **Seeds**: Raw data CSV files (raw_customers, raw_orders, raw_payments)
- **Staging Models**: Data cleaning and transformation layers
- **Mart Models**: Final business logic models (customers, orders)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your PostgreSQL connection in `profiles.yml`

3. Test connection:
```bash
dbt debug
```

4. Load seed data:
```bash
dbt seed
```

5. Run models:
```bash
dbt run
```

6. Run tests:
```bash
dbt test
```

## Database Connection

This project connects to a PostgreSQL database on Neon.tech.
Connection details are configured in `profiles.yml`.

## Models

- `stg_customers`: Staging layer for customer data
- `stg_orders`: Staging layer for order data
- `stg_payments`: Staging layer for payment data
- `customers`: Final customer dimension with order statistics
- `orders`: Final orders fact table with payment breakdowns

