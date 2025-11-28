# Mycelium HTTP Tools

A python library to integrate python APIs in Mycelium API Gateway.

## Installation

### Basic Installation

Install the core library without optional dependencies:

```bash
pip install mycelium-http-tools
```

### With FastAPI Support

To use the FastAPI middleware for profile extraction, install with the FastAPI extra:

```bash
pip install mycelium-http-tools[fastapi]
```

This will install the additional dependencies:

- `fastapi>=0.104.0,<1.0.0`
- `zstandard>=0.25.0,<0.26.0`

### Development Installation

For development with all dependencies:

```bash
pip install mycelium-http-tools[dev,fastapi]
```

## Usage

### Basic Usage

```python
from myc_http_tools.models.profile import Profile
from myc_http_tools.models.owner import Owner

# Create and use Profile objects
profile = Profile(
    acc_id="123e4567-e89b-12d3-a456-426614174000",
    is_subscription=True,
    is_staff=True,
    is_manager=False,
    owner_is_active=True,
    account_is_active=True,
    account_was_approved=True,
    account_was_archived=False,
    account_was_deleted=False,
    owners=[Owner(...)]
)
```

### FastAPI Integration

If you installed with FastAPI support, you have several options:

#### Option 1: Using Dependency Injection (Recommended)

```python
from fastapi import FastAPI, Depends
from myc_http_tools.fastapi import get_profile_from_header, get_profile_from_header_required

app = FastAPI()

# Optional profile (returns None if header missing in development)
@app.get("/")
async def my_route(profile: Profile | None = Depends(get_profile_from_header)):
    if profile:
        related_accounts = profile \
            .with_read_access() \
            .on_tenant(tenant_id) \
            .with_roles(["admin"]) \
            .on_account(account_id) \
            .get_related_account_or_error()
        # ... use the related accounts
    else:
        return {"message": "No profile available"}

# Required profile (raises error if header missing)
@app.get("/protected")
async def protected_route(profile: Profile = Depends(get_profile_from_header_required)):
    related_accounts = profile \
        .with_read_access() \
        .on_tenant(tenant_id) \
        .with_roles(["admin"]) \
        .on_account(account_id) \
        .get_related_account_or_error()
    # ... use the related accounts
```

#### Option 2: Using Middleware

```python
from fastapi import FastAPI
from fastapi.middleware.base import BaseHTTPMiddleware
from myc_http_tools.fastapi import profile_middleware

app = FastAPI()
app.add_middleware(BaseHTTPMiddleware, dispatch=profile_middleware)

@app.get("/")
async def my_route(request: Request):
    profile = request.state.profile  # Profile extracted from x-mycelium-profile header
    # ... use the profile
```

#### Option 3: Manual Extraction

```python
from fastapi import FastAPI, Depends
from myc_http_tools.fastapi import get_profile_from_request

app = FastAPI()

@app.get("/")
async def my_route(request: Request):
    profile = get_profile_from_request(request)
    # ... use the profile
```

## Features

- **Profile Management**: Core Profile model with filtering and permission management
- **FastAPI Middleware** (optional): Extract profiles from HTTP headers
- **Flexible Installation**: Install only what you need

## License

Apache 2.0
