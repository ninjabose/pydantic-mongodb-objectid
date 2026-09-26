# Pydantic MongoDB ObjectId

A reusable Pydantic custom type for seamless MongoDB `ObjectId` validation and serialization in FastAPI applications.

## The Problem

MongoDB uses `bson.ObjectId` for document IDs, while APIs commonly expose IDs as strings.

Without custom handling, Pydantic may not know how to generate a schema for `ObjectId`:

```text
Unable to generate pydantic-core schema for <class 'bson.objectid.ObjectId'>
```

This project provides a `PyObjectId` type that bridges the gap between MongoDB and Pydantic.

## What It Does

`PyObjectId` provides:

- ✅ MongoDB `ObjectId` validation
- ✅ String → `ObjectId` conversion
- ✅ `ObjectId` → string serialization
- ✅ Pydantic schema integration
- ✅ Clean JSON responses
- ✅ Works with FastAPI response models

## Installation

```bash
pip install pydantic pymongo
```

Copy `PyObjectId` into your project:

```text
app/
└── schemas/
    └── types/
        └── object_id.py
```

## Usage

```python
from pydantic import BaseModel, Field
from app.schemas.types.object_id import PyObjectId


class UserResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    username: str
```

A MongoDB document can contain:

```python
{
    "_id": ObjectId("68a123456789abcdef123456"),
    "username": "bose"
}
```

Pydantic can validate and serialize it for an API response as:

```json
{
    "id": "68a123456789abcdef123456",
    "username": "bose"
}
```

The database continues to use the native MongoDB `ObjectId`.

## How It Works

The implementation uses Pydantic's custom schema hook:

```python
__get_pydantic_core_schema__
```

This tells Pydantic how to:

1. Validate incoming values.
2. Convert valid strings into `ObjectId`.
3. Accept existing `ObjectId` instances.
4. Serialize `ObjectId` values as strings.

Conceptually:

```text
MongoDB
   │
   │ ObjectId
   ▼
PyObjectId
   │
   ├── Validation
   └── Serialization
   │
   ▼
Pydantic
   │
   ▼
JSON API
   │
   │ "68a123..."
   ▼
Client
```

## Why Not `arbitrary_types_allowed=True`?

Pydantic can be configured to allow arbitrary types, but that doesn't explain how the custom type should be validated or serialized.

`PyObjectId` explicitly defines those behaviors instead.

This keeps the integration type-specific and reusable.

## Example

```python
from bson import ObjectId
from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: PyObjectId = Field(alias="_id")
    username: str


user = UserResponse(
    _id=ObjectId(),
    username="bose"
)

print(user.id)
print(user.model_dump())
print(user.model_dump_json())
```

## Testing

The project includes tests covering:

- Valid `ObjectId` strings
- Invalid `ObjectId` strings
- Existing `ObjectId` instances
- Pydantic validation
- Serialization to JSON

Run:

```bash
pytest
```

## Why This Exists

This was built while working with **FastAPI + Pydantic + native async PyMongo** and dealing with the boundary between MongoDB's native `ObjectId` type and Pydantic's validation/serialization system.

Rather than allowing arbitrary types globally, this implementation teaches Pydantic exactly how `ObjectId` should behave.

## License

MIT