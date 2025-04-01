import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server import Post, Base
from repository import PostRepository

@pytest.fixture
def test_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def repo(test_session):
    class TestRepo(PostRepository):
        def __init__(self):
            self._session = test_session

        def get_db(self):
            return self._session

        def session_scope(self):
            yield self._session

    return TestRepo()

def test_create_post(repo):
    post = repo.create_post(
        title="Test",
        description="Desc",
        creator_id=1,
        is_private=False,
        tags=["one", "two"]
    )
    assert post.id == 1
    assert post.title == "Test"
    assert post.creator_id == 1
    assert post.is_private is False
    assert post.to_proto().tags == ["one", "two"]

def test_update_post(repo):
    created = repo.create_post(
        title="Before",
        description="Old",
        creator_id=1,
        is_private=False,
        tags=["a"]
    )

    updated = repo.update_post(
        id=created.id,
        updater_id=1,
        title="After",
        description="New",
        is_private=True,
        tags=["b", "c"]
    )

    assert updated.title == "After"
    assert updated.description == "New"
    assert updated.is_private is True
    assert updated.to_proto().tags == ["b", "c"]

def test_get_post(repo):
    post = repo.create_post(
        title="Hidden",
        description="Private",
        creator_id=1,
        is_private=True,
        tags=[]
    )

    # visible to owner
    assert repo.get_post(post.id, requester_id=1).title == "Hidden"

    # not visible to others
    with pytest.raises(PermissionError):
        repo.get_post(post.id, requester_id=999)

def test_delete_post(repo):
    post = repo.create_post(
        title="To delete",
        description="will go",
        creator_id=1,
        is_private=False,
        tags=[]
    )

    repo.delete_post(post.id, deleter_id=1)

    with pytest.raises(Exception):
        repo.get_post(post.id, requester_id=1)

def test_list_posts(repo):
    repo.create_post("Public", "Post 1", 1, False, [])
    repo.create_post("Private", "Post 2", 2, True, [])
    repo.create_post("Mine", "Post 3", 3, True, [])

    posts = repo.list_posts(page=1, page_size=10, requester_id=3)
    titles = [p.title for p in posts]

    assert "Public" in titles
    assert "Mine" in titles
    assert "Private" not in titles
