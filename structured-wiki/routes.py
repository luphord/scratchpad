"""
GET /show/page/123  # show page with ID 123

GET /edit/page/123  # get editing mask for page with ID 123
PUT /edit/page/123  # submit form to update page with ID 123

GET /edit/page  # get editing mask for a new page (no ID yet)
POST /edit/page  # submit form to create a new page


GET /list/type  # list all type definitions

GET /edit/type/mytype  # get editing mask (form) for type definition of type mytype
PUT /edit/type/mytype  # submit form to update type definition of type mytype

GET /edit/type  # get editing mask (form) for a new type (no name yet)
POST /edit/type  # submit form to create a new type


GET /list/object/mytype  # list all objects of type mytype

GET /show/object/mytype/111  # show object with ID 111 as mytype

GET /edit/object/mytype/111  # get editing mask (form) for type mytype for object 111
PATCH /edit/object/mytype/111  # submit form to update object 111

GET /edit/object/mytype  # get editing mask (form) for type mytype for a new object (no ID yet)
POST /edit/object/mytype  # submit form to create a new instance of mytype
"""