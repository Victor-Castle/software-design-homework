"""
数据库模型定义
使用SQLAlchemy ORM，SQLite数据库
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'library.db')
DATABASE_URL = f"sqlite:///{DB_PATH}"

# 创建引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), default="reader")  # reader / admin
    max_borrow = Column(Integer, default=5)       # 最大借阅数量
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    borrow_records = relationship("BorrowRecord", back_populates="user")

class Book(Base):
    """图书表"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    isbn = Column(String(20), unique=True, nullable=False)
    publisher = Column(String(100), nullable=True)
    published_year = Column(Integer, nullable=True)
    category = Column(String(50), nullable=True, index=True)
    location = Column(String(50), nullable=True)  # 馆藏位置
    total_copies = Column(Integer, default=1)      # 总复本数
    available_copies = Column(Integer, default=1)   # 可借复本数
    description = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    borrow_records = relationship("BorrowRecord", back_populates="book")

class BorrowRecord(Base):
    """借阅记录表"""
    __tablename__ = "borrow_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(String(20), default="borrowing")  # borrowing / returned / overdue
    is_overdue = Column(Boolean, default=False)

    user = relationship("User", back_populates="borrow_records")
    book = relationship("Book", back_populates="borrow_records")

# 初始化数据库
def init_database():
    """创建所有表并插入测试数据"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # 检查是否已有数据
    if db.query(User).count() == 0:
        # 插入测试用户
        test_users = [
            User(username="zhangsan", password="123456", role="reader", max_borrow=5, email="zhangsan@example.com"),
            User(username="lisi", password="123456", role="reader", max_borrow=5, email="lisi@example.com"),
            User(username="admin", password="admin123", role="admin", max_borrow=100, email="admin@library.com"),
        ]
        db.add_all(test_users)
        
        # 插入测试图书
        test_books = [
            Book(title="三体", author="刘慈欣", isbn="9787536692930", publisher="重庆出版社",
                 published_year=2008, category="科幻", location="普通阅览室A区",
                 total_copies=5, available_copies=3, description="中国科幻文学里程碑之作"),
            Book(title="三体II：黑暗森林", author="刘慈欣", isbn="9787536692947", publisher="重庆出版社",
                 published_year=2008, category="科幻", location="普通阅览室A区",
                 total_copies=3, available_copies=2, description="三体系列第二部"),
            Book(title="三体III：死神永生", author="刘慈欣", isbn="9787536692954", publisher="重庆出版社",
                 published_year=2010, category="科幻", location="普通阅览室A区",
                 total_copies=3, available_copies=2, description="三体系列最终部"),
            Book(title="深入理解计算机系统", author="Randal E. Bryant", isbn="9787111544937", publisher="机械工业出版社",
                 published_year=2016, category="计算机科学", location="专业阅览室B区",
                 total_copies=2, available_copies=1, description="计算机系统基础经典教材"),
            Book(title="Java核心技术", author="凯·S·霍斯特曼", isbn="9787111561033", publisher="机械工业出版社",
                 published_year=2019, category="计算机科学", location="专业阅览室B区",
                 total_copies=3, available_copies=2, description="Java学习必读"),
            Book(title="三国演义", author="罗贯中", isbn="9787020008728", publisher="人民文学出版社",
                 published_year=1953, category="古典文学", location="普通阅览室C区",
                 total_copies=4, available_copies=4, description="中国四大名著之一"),
            Book(title="活着", author="余华", isbn="9787506365437", publisher="作家出版社",
                 published_year=1993, category="当代文学", location="普通阅览室C区",
                 total_copies=3, available_copies=2, description="余华代表作"),
        ]
        db.add_all(test_books)
        
        # 插入一些借阅记录（已借出）
        test_records = [
            BorrowRecord(user_id=1, book_id=1, borrow_date=datetime(2026, 6, 20),
                         due_date=datetime(2026, 7, 20), status="borrowing"),
            BorrowRecord(user_id=1, book_id=4, borrow_date=datetime(2026, 6, 15),
                         due_date=datetime(2026, 7, 15), status="borrowing"),
            BorrowRecord(user_id=2, book_id=2, borrow_date=datetime(2026, 7, 1),
                         due_date=datetime(2026, 8, 1), status="borrowing"),
        ]
        db.add_all(test_records)
        
        db.commit()
        print("✅ 数据库初始化完成，已插入测试数据")
    
    db.close()
