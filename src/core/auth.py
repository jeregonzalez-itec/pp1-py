import bcrypt
import jwt
# Funciones utilitarias para la autenticación


def get_password_hash(password: str) -> str:
    """
    Función que a partir de una contraseña en texto plano, genera un hash.
    Convierte el str plano en bytes, genera un salt único y la 'encripta'.
    Devuelve el hash creado a partir de la contraseña. Es lo hay que guardar en la DB.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()  # Identificador único para generar el hash
    hashed_pwd = bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")
    return hashed_pwd


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Chequea si la contraseña en texto plano coincide con la contraseña hasheada.
    No se 'des-encripta', devuelve True o False.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )

class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 30):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes
    def create_access_token(self, data: dict) -> str:
        """
        Crea un token JWT firmado.
        'data' debe contener al menos el 'sub' (subject), que suele ser el email o ID.
        """
        to_encode = data.copy()

        # Calculamos la fecha límite usando timezone.utc para evitar problemas de zonas horarias
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})

        # jwt.encode empaqueta el header, el payload y firma el token
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt
    def verify_token(self, token: str) -> dict:
        """
        Decodifica el token. Si algo falla, interrumpe la petición con un error HTTP 401.
        """
        try:
            # jwt.decode verifica automáticamente la firma y la fecha de expiración ('exp')
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload

        except jwt.ExpiredSignatureError:
            # El token es real, pero ya caducó
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="El token ha expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            # El token fue alterado, está mal formado o firmado con otra clave
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

jwt_manager = JWTManager(
    secret_key="clave_super_secreta_development",
    expire_minutes=60 
)