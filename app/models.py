from app import db
import enum


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


class Assigned_Office(db.Model):
    __tablename__ = 'assigned_office'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        return '<Assigned Office: %r>' % (self.name)

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
        return '[{}-{}] {:10,.2f}'.format(self.sg, self.step, self.amount)


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

    def __str__(self):
        return '[{}] {}'.format(self.itemno, self.position.name)


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    employee_no = db.Column(db.String(20), unique=True)
    last_name = db.Column(db.String(80), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    middle_name = db.Column(db.String(80))
    birth_date = db.Column(db.Date)
    etd_nfa = db.Column(db.Date)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    @property
    def full_name(self):
        return self.__str__()

    def __str__(self):
        return ', '.join(filter(None, [self.last_name, self.first_name,
                                       self.middle_name]))


class Employee_Detail(db.Model):
    __tablename__ = 'employee_detail'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer,
        db.ForeignKey('employee.id', ondelete='CASCADE'))
    plantilla_id = db.Column(db.Integer,
        db.ForeignKey('plantilla.id', ondelete='CASCADE'))
    salary_id = db.Column(db.Integer,
        db.ForeignKey('salary.id', ondelete='CASCADE'))
    assigned_office_id = db.Column(db.Integer,
        db.ForeignKey('assigned_office.id', ondelete='CASCADE'))

    employee = db.relationship('Employee')
    plantilla = db.relationship('Plantilla')
    salary = db.relationship('Salary')
    assigned_office = db.relationship('Assigned_Office')


class Payroll(db.Model):
    __tablename__ = 'payroll'
    id = db.Column(db.Integer, primary_key=True)
    office_id = db.Column(db.Integer,
            db.ForeignKey('office.id', ondelete='CASCADE'))
    assigned_office_id = db.Column(db.Integer,
            db.ForeignKey('assigned_office.id', ondelete='CASCADE'))
    payroll_type_id = db.Column(db.Integer,
            db.ForeignKey('payroll_type.id', ondelete='CASCADE'))
    date = db.Column(db.Date, default=db.func.current_timestamp())
    period = db.Column(db.String(80), nullable=False)
    is_open = db.Column(db.Boolean, default=True)

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    office = db.relationship('Office')
    payroll_type = db.relationship('Payroll_Type')
    employees = db.relationship('Employee', secondary='payroll_employees')


class Payroll_Type(db.Model):
    __tablename__ = 'payroll_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)

    earnings = db.relationship('Earnings', secondary='payroll_type_earnings',
                               backref='payroll_types')

    def __str__(self):
        return self.name


class Payroll_Type_Earnings(db.Model):
    __tablename__ = 'payroll_type_earnings'
    id = db.Column(db.Integer, primary_key=True)
    payroll_type_id = db.Column(db.Integer,
            db.ForeignKey('payroll_type.id', ondelete='CASCADE'))
    earnings_id = db.Column(db.Integer,
            db.ForeignKey('earnings.id', ondelete='CASCADE'))

    earnings = db.relationship('Earnings')


class payment_types(enum.Enum):
    PAY = 'Payroll'
    REM = 'Remittance'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

    def __str__(self):
        return self.name

    def __html__(self):
        return self.value


class Earnings(db.Model):
    __tablename__ = 'earnings'
    id = db.Column(db.Integer, primary_key=True)
    sequence = db.Column(db.Float)
    name = db.Column(db.String(80), nullable=False, unique=True)
    formula = db.Column(db.String(255))
    fixed_amount = db.Column(db.Numeric(15, 2))
    payment_type = db.Column(db.String(3), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __str__(self):
        return self.name


class Deductions(db.Model):
    __tablename__ = 'deductions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    active = db.Column(db.Boolean, default=True)


class Payroll_Earnings(db.Model):
    __tablename__ = 'payroll_earnings'
    id = db.Column(db.Integer, primary_key=True)
    payroll_id = db.Column(db.Integer,
            db.ForeignKey('payroll.id', ondelete='CASCADE'))
    employee_id = db.Column(db.Integer,
            db.ForeignKey('employee.id', ondelete='CASCADE'))
    earnings_id = db.Column(db.Integer,
            db.ForeignKey('earnings.id', ondelete='CASCADE'))
    amount = db.Column(db.Numeric(15, 2))

    employee = db.relationship('Employee')


class Payroll_Employees(db.Model):
    __tablename__ = 'payroll_employees'
    id = db.Column(db.Integer, primary_key=True)
    payroll_id = db.Column(db.Integer,
            db.ForeignKey('payroll.id', ondelete='CASCADE'))
    employee_id = db.Column(db.Integer,
            db.ForeignKey('employee.id', ondelete='CASCADE'))

    employee = db.relationship('Employee')


class Payroll_Group(db.Model):
    __tablename__ = 'payroll_group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class Payroll_Group_Employee(db.Model):
    __tablename__ = 'payroll_group_employee'
    id = db.Column(db.Integer, primary_key=True)
    payroll_group_id = db.Column(db.Integer,
        db.ForeignKey('payroll_group.id', ondelete='CASCADE'))
    employee_id = db.Column(db.Integer,
        db.ForeignKey('employee.id', ondelete='CASCADE'))
    employee = db.relationship('Employee')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
