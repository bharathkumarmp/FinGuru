from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, TokenResponse


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ============================================================
# DEMO USERS
# ============================================================
# Hackathon MVP authentication.
#
# Login credentials:
# Mobile:   9876543210
# Password: FinGuru@123
#
# Later this can be replaced with database authentication.
# ============================================================

DEMO_USERS = {
    "9876543210": {
        "id": 1,
        "mobile": "9876543210",
        "password": "FinGuru@123",
        "role": "customer",
    },
}


# ============================================================
# TOKEN
# ============================================================

def create_access_token(
    user_id: int,
    mobile: str,
    role: str,
) -> str:
    """
    Creates a simple demo access token.

    For the hackathon MVP this is sufficient to establish
    the frontend/backend authentication flow.

    Production version should use the project's JWT
    implementation with expiration and signing.
    """

    return f"finguru-demo-token-{user_id}-{role}"


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login with mobile number and password",
)
def login(request: LoginRequest):
    """
    Authenticate a FinGuru customer.

    Request:
        {
            "mobile": "9876543210",
            "password": "FinGuru@123"
        }

    Response:
        {
            "access_token": "...",
            "token_type": "bearer"
        }
    """

    # --------------------------------------------------------
    # Normalize mobile number
    # --------------------------------------------------------

    mobile = request.mobile.strip()

    # Remove +91 if frontend sends it
    if mobile.startswith("+91"):
        mobile = mobile[3:]

    # Remove spaces
    mobile = mobile.replace(" ", "")

    # --------------------------------------------------------
    # Validate mobile number
    # --------------------------------------------------------

    if not mobile.isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number must contain only digits",
        )

    if len(mobile) != 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number must contain 10 digits",
        )

    # --------------------------------------------------------
    # Find user
    # --------------------------------------------------------

    user = DEMO_USERS.get(mobile)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid mobile number or password",
        )

    # --------------------------------------------------------
    # Verify password
    # --------------------------------------------------------

    if request.password != user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid mobile number or password",
        )

    # --------------------------------------------------------
    # Generate token
    # --------------------------------------------------------

    access_token = create_access_token(
        user_id=user["id"],
        mobile=user["mobile"],
        role=user["role"],
    )

    # --------------------------------------------------------
    # Return token
    # --------------------------------------------------------

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )


# ============================================================
# CURRENT USER
# ============================================================

@router.get(
    "/me",
    summary="Get demo authenticated user",
)
def get_current_user():
    """
    Returns the demo customer information.

    This endpoint is useful for the frontend while we are
    building the hackathon MVP.
    """

    return {
        "id": 1,
        "mobile": "9876543210",
        "role": "customer",
    }