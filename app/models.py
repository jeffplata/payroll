from app import db


class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<Section %r>' % (self.name)

    def __str__(self):
        return self.name


class Office(db.Model):
    __tablename__ = 'office'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<Office: %r>' % (self.name)

    def __str__(self):
        return self.name


class Salary_reference(db.Model):
    __tablename__ = 'salary_reference'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<SalRef: %r>' % (self.name)

    def __str__(self):
        return self.name


class Salary(db.Model):
    __tablename__ = 'salary'
    id = db.Column(db.Integer, primary_key=True)
    sg = db.Column(db.Integer, nullable=False)
    step = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    salary_reference_id = db.Column(db.Integer,
            db.ForeignKey('salary_reference.id', ondelete='CASCADE'))

    salary_reference = db.relationship('Salary_reference', backref='reference')

    def __repr__(self):
        return '<Salary: %r/%r/%r>' % (self.sg, self.step, self.amount)

    def __str__(self):
        return '{:2} {:2} {:10,.2f}'.format(self.sg, self.step, self.amount)


class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    sg = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __str__(self):
        return self.name


class Plantilla_type(db.Model):
    __tablename__ = 'plantilla_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __str__(self):
        return self.name


class Plantilla(db.Model):
    __tablename__ = 'plantilla'
    id = db.Column(db.Integer, primary_key=True)
    itemno = db.Column(db.String(20), nullable=False, unique=True)
    plantilla_type_id = db.Column(db.Integer,
            db.ForeignKey('plantilla_type.id', ondelete='CASCADE'))
    position_id = db.Column(db.Integer,
            db.ForeignKey('position.id', ondelete='CASCADE'))
    office_id = db.Column(db.Integer,
            db.ForeignKey('office.id', ondelete='CASCADE'))
    section_id = db.Column(db.Integer,
            db.ForeignKey('section.id', ondelete='CASCADE'))
    sg = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    plantilla_type = db.relationship('Plantilla_type')
    position = db.relationship('Position')
    office = db.relationship('Office')
    section = db.relationship('Section')
