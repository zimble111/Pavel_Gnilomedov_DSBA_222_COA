import grpc
from concurrent import futures
import json
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base
from posts_pb2 import PostResponse, DeletePostResponse, ListPostsResponse
import posts_pb2_grpc
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    creator_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    is_private = Column(Boolean, default=False)
    tags = Column(String)  # JSON string

    def to_proto(self):
        return PostResponse(
            id=self.id,
            title=self.title,
            description=self.description,
            creator_id=self.creator_id,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
            is_private=self.is_private,
            tags=json.loads(self.tags or "[]")
        )

Base.metadata.create_all(engine)

class PostService(posts_pb2_grpc.PostServiceServicer):
    def CreatePost(self, request, context):
        db = SessionLocal()
        post = Post(
            title=request.title,
            description=request.description,
            creator_id=request.creator_id,
            is_private=request.is_private,
            tags=json.dumps(request.tags)
        )
        db.add(post)
        db.commit()
        db.refresh(post)
        db.close()
        return post.to_proto()

    def GetPost(self, request, context):
        db = SessionLocal()
        post = db.query(Post).filter(Post.id == request.id).first()
        db.close()
        if not post or (post.is_private and post.creator_id != request.requester_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found or forbidden")
        return post.to_proto()

    def UpdatePost(self, request, context):
        db = SessionLocal()
        post = db.query(Post).filter(Post.id == request.id).first()
        if not post or post.creator_id != request.updater_id:
            db.close()
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Not allowed")
        post.title = request.title or post.title
        post.description = request.description or post.description
        post.is_private = request.is_private
        post.tags = json.dumps(request.tags)
        db.commit()
        db.refresh(post)
        db.close()
        return post.to_proto()

    def DeletePost(self, request, context):
        db = SessionLocal()
        post = db.query(Post).filter(Post.id == request.id).first()
        if not post or post.creator_id != request.deleter_id:
            db.close()
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Not allowed")
        db.delete(post)
        db.commit()
        db.close()
        return DeletePostResponse(message="Deleted")

    def ListPosts(self, request, context):
        db = SessionLocal()
        query = db.query(Post).filter(
            (Post.is_private == False) | (Post.creator_id == request.requester_id)
        )
        posts = query.offset((request.page - 1) * request.page_size).limit(request.page_size).all()
        db.close()
        return ListPostsResponse(posts=[p.to_proto() for p in posts])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    posts_pb2_grpc.add_PostServiceServicer_to_server(PostService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("PostService gRPC server running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
import grpc
from concurrent import futures
import json
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base
from posts_pb2 import PostResponse, DeletePostResponse, ListPostsResponse
import posts_pb2_grpc
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    creator_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    is_private = Column(Boolean, default=False)
    tags = Column(String)  # JSON string

    def to_proto(self):
        return PostResponse(
            id=self.id,
            title=self.title,
            description=self.description,
            creator_id=self.creator_id,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
            is_private=self.is_private,
            tags=json.loads(self.tags or "[]")
        )

Base.metadata.create_all(engine)

class PostService(posts_pb2_grpc.PostServiceServicer):
    def CreatePost(self, request, context):
        db = SessionLocal()
        post = Post(
            title=request.title,
            description=request.description,
            creator_id=request.creator_id,
            is_private=request.is_private,
            tags=json.dumps(request.tags)
        )
        db.add(post)
        print("🧠 BEFORE COMMIT:", post.id)
        db.commit()
        db.refresh(post)
        print("🧠 AFTER REFRESH:", post.id)
        db.close()
        return post.to_proto()

    docker
    compose
    restart
    post_service
    def GetPost(self, request, context):
        db = SessionLocal()
        post = db.query(Post).filter(Post.id == request.id).first()
        db.close()
        if not post or (post.is_private and post.creator_id != request.requester_id):
            context.abort(grpc.StatusCode.NOT_FOUND, "Post not found or forbidden")
        return post.to_proto()

    def UpdatePost(self, request, context):
        db = SessionLocal()
        post = db.query(Post).filter(Post.id == request.id).first()
        if not post or post.creator_id != request.updater_id:
            db.close()
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Not allowed")
        post.title = request.title or post.title
        post.description = request.description or post.description
        post.is_private = request.is_private
        post.tags = json.dumps(request.tags)
        db.commit()
        db.refresh(post)
        db.close()
        return post.to_proto()

    def DeletePost(self, request, context):
        db = SessionLocal()
        post = db.query(Post).filter(Post.id == request.id).first()
        if not post or post.creator_id != request.deleter_id:
            db.close()
            context.abort(grpc.StatusCode.PERMISSION_DENIED, "Not allowed")
        db.delete(post)
        db.commit()
        db.close()
        return DeletePostResponse(message="Deleted")

    def ListPosts(self, request, context):
        db = SessionLocal()
        query = db.query(Post).filter(
            (Post.is_private == False) | (Post.creator_id == request.requester_id)
        )
        posts = query.offset((request.page - 1) * request.page_size).limit(request.page_size).all()
        db.close()
        return ListPostsResponse(posts=[p.to_proto() for p in posts])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    posts_pb2_grpc.add_PostServiceServicer_to_server(PostService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("PostService gRPC server running on port 50051")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
