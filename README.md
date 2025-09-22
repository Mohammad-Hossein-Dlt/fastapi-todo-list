ENV File Parameters

Put it next to the app

```
EXTERNAL_FASTAPI_PORT = 80
INTERNAL_FASTAPI_PORT = 8000

DB_STACK = postgresql # postgresql, mongo_db

MONGO_HOST = mongo-db
MONGO_PORT = 27017
MONGO_INITDB_ROOT_USERNAME = root
MONGO_INITDB_ROOT_PASSWORD = rootpassword
MONGO_INITDB_DATABASE = db

POSTGRES_HOST = postgres-db
POSTGRES_PORT = 5432
POSTGRES_USER = admin
POSTGRES_PASSWORD = adminpassword
POSTGRES_DB = db

PGADMIN_DEFAULT_EMAIL = admin@example.com
PGADMIN_DEFAULT_PASSWORD = secret

JWT_SECRET = 5fd4a7c9-7b61-49bf-8aea-ae8c53727290
JWT_ALGORITHM = HS256
JWT_EXPIRATION_MINUTES = 10
```

To Run

```
fastapi dev app/src/main.py
```

## App architecture description

### Infra Layer

In this layer, the application infrastructure is defined, such as:

- Authentication utilities such as token creation, management, and validation

- Database client and its models (tables)

- Errors related to this layer and other layers

  - include status code and message

- Services for interacting with external APIs

  - include interfaces and their implementation

- Fastapi config such as

  - middleware
  - tasks that should be run on startup or shutdown, such as create and close database client
  - implement some states based on settings loaded from .env in main app, to have access them throughout the entire project

- Mixin classes

- Application settings load from the `.env` file
  - load with pydantic_settings

```
infra/
│
├── auth/
│   └── <files or directories...>
│
├── db/
│   ├── redis/
│   │   └── <files or directories...>
│   │
│   ├── mongodb/
│   │   └── <files or directories...>
│   │
│   └── sqlite/
│       └── <files or directories...>
│
├── exceptions/
│   └── <files...>
│
├── external_api/
│   ├── interface/
│   │   └── <files...>
│   │
│   └── service/
│       └── <files...>
│
├── fastapi_config/
│   └── <files...>
│
├── mixins/
│   └── <files...>
│
└── settings/
    └── <files...>
```

### Domain Layer

In this layer, data models are defined that are only used inside the application, meaning between layers, for transferring data.

```
domain/
├── mock_data/
│   └── <files...>
│
└── schemas/
    └── <schema_group_name>/
       └── <files...>
```

### Models Layer

In this layer, data models are defined that are only used for receiving or sending data to the client.

```
models/
├── filter/
│   └── <files...>
│
└── schemas/
    └── <schema_group_name>/
        └── <files...>

```

### Repo Layer

In this layer, communication with the database is handled.
Repository classes are defined here, whose methods provide interaction with the database.
Each repository class inherits from an interface defined in this layer.
Interfaces define the structure of database communication, so we can have multiple repository classes based on a single interface and use them for dependency injection.

```
repo/
├── interface/
│   └── <files...>
│
└── <implementation_name>/
    └── <files...>
```

Naming implementations can be based on:

- **Storage type** — for example: `sql`, `nosql`

```
repo/
├── interface/
│   └── <files...>
│
├── sql/
│   └── <files...>
│
└── nosql/
    └── <files...>
```

- **Storage name** — for example: `postgresql`, or `mongodb`.

```
repo/
├── interface/
│   └── <files...>
│
├── postgresql/
│   └── <files...>
│
└── mongodb/
    └── <files...>
```

### Routes Layer

In this layer, endpoints are defined along with their dependencies, response statuses, and other endpoint-related configurations.

```
routes/
├── api_endpoints/
│   ├── <endpoint_group_name>/
│   │   └── <files...>
│   │
│   ├── <endpoint_group_name>/
│   │   └── <files...>
│   │
│   └── main_router.py
│
├── depends/
│   └── <files...>
│
└── http_response/
    └── <files...>
```

### Usecase Layer

In this layer, the application’s business logic is defined.
This layer acts as an important bridge between endpoints in the Routes layer, the database in the Repo layer, and external APIs in the Infra layer.

```
usecase/
├── <usecase_group_name>/
│   └── <files...>
│
└── <usecase_group_name>/
    └── <files...>
```

#### Note

The layers are not limited to the mentioned items and can also include other related configurations.
