from src.utils import required_role
from http import HTTPStatus

def test_required_role_success(mocker):
    # Arrange
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"
    
    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)
    
    decorated_function = required_role("admin")(lambda: 'success')
    
    # Act
    result = decorated_function()
    
    # Assert
    assert result == 'success'
    
    
def test_required_role_fail(mocker):
    # Arrange
    mock_user = mocker.Mock()
    mock_user.role.name = "user"
    
    mocker.patch("src.utils.get_jwt_identity")
    mocker.patch("src.utils.db.get_or_404", return_value=mock_user)
    
    decorated_function = required_role("admin")(lambda: 'success')
    
    # Act
    result = decorated_function()
    
    # Assert
    assert result == ({"message": "Permission denied"}, HTTPStatus.FORBIDDEN)
    