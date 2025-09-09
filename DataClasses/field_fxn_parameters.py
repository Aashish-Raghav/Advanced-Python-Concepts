from dataclasses import dataclass,field
import uuid
from datetime import datetime

@dataclass
class BlogPost:
    title : str
    content : str

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at : datetime = field(default_factory=datetime.now)

    tags : list[str] = field(default_factory=list)
    metadata : dict[str,str] = field(default_factory=dict)

    internal_notes : str = field(default="", repr=False)

    view_count : int = field(default=0,compare=False)

    slug : str = field(init=False)

    def __post_init__(self):
        self.slug = self.title.lower().replace(' ', '-')


post1 = BlogPost("Hello World", "This is my first post")
post2 = BlogPost("Python Tips", "Some useful Python tips")

print(post1.id != post2.id)  # True (unique IDs)
print(post1.created_at != post2.created_at)  # Likely True (different timestamps)
print(post1.slug)  # hello-world
print(post2.slug)  # python-tips

post1.tags.append("introduction")
post2.tags.append("python")
print(post1.tags)  # ['introduction']
print(post2.tags)  # ['python']