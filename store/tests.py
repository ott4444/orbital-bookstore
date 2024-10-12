import pytest
from django.contrib.auth import get_user_model

# Get the User model
User = get_user_model()

# 1. Test Create (C)
@pytest.mark.django_db
def test_create_user():
    user = User.objects.create(username='testuser', email='test@example.com')
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'

# 2. Test Read (R)
@pytest.mark.django_db
def test_read_user():
    user = User.objects.create(username='testuser', email='test@example.com')
    fetched_user = User.objects.get(username='testuser')
    assert fetched_user.email == 'test@example.com'

# 3. Test Update (U)
@pytest.mark.django_db
def test_update_user():
    user = User.objects.create(username='testuser', email='test@example.com')
    user.email = 'newemail@example.com'
    user.save()
    updated_user = User.objects.get(username='testuser')
    assert updated_user.email == 'newemail@example.com'

# 4. Test Delete (D)
@pytest.mark.django_db
def test_delete_user():
    user = User.objects.create(username='testuser', email='test@example.com')
    user.delete()
    with pytest.raises(User.DoesNotExist):
        User.objects.get(username='testuser')

# 5. Test if user already exists (Edge case)
@pytest.mark.django_db
def test_user_exists():
    User.objects.create(username='testuser', email='test@example.com')
    exists = User.objects.filter(username='testuser').exists()
    assert exists is True
