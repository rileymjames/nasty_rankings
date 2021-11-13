from .. import db


class Scenario(db.Model):
    __tablename__ = 'scenario'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    programs = db.relationship('Program', back_populates='scenario', cascade="all, delete")
    incentives = db.relationship('Incentive', back_populates='scenario', cascade="all, delete")
    forecasts = db.relationship('Forecast', back_populates='scenario', cascade="all, delete")

    def __repr__(self):
        return '<Scenario %r>' % self.name


class Program(db.Model):
    __tablename__ = 'program'

    id = db.Column(db.Integer, primary_key=True)

    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    scenario = db.relationship('Scenario', back_populates='programs')

    name = db.Column(db.String(80), nullable=False)
    budget_type = db.Column(db.String(50), nullable=True)
    budget = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return '<Program %r>' % self.name


class Incentive(db.Model):
    __tablename__ = 'incentive'

    id = db.Column(db.Integer, primary_key=True)

    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    scenario = db.relationship('Scenario', back_populates='incentives')

    measure_id = db.Column(db.Integer, nullable=False)
    bldgtype_id = db.Column(db.Integer, nullable=False)
    segment_id = db.Column(db.Integer, nullable=False)
    measure_desc = db.Column(db.String(200), nullable=False)
    bldgtype_desc = db.Column(db.String(200), nullable=False)
    program_desc = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    rebate = db.Column(db.Float)
    unit = db.Column(db.String(10))

    def __repr__(self):
        return '<Incentive %r>' % self.id


class Forecast(db.Model):
    __tablename__ = 'forecast'

    id = db.Column(db.Integer, primary_key=True)

    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'))
    scenario = db.relationship('Scenario', back_populates='forecasts')

    year = db.Column(db.Integer)

    measure_id = db.Column(db.Integer, nullable=False)
    measure_desc = db.Column(db.String(200), nullable=False)
    bldgtype_id = db.Column(db.Integer, nullable=False)
    bldgtype_desc = db.Column(db.String(200), nullable=False)
    program = db.Column(db.String(100), nullable=False)
    segment_id = db.Column(db.Integer, nullable=False)
    segment_desc = db.Column(db.String(200), nullable=False)
    sector = db.Column(db.String(100), nullable=False)

    total_shipments = db.Column(db.Float)
    annual_incentive = db.Column(db.Float)
    annual_energy_savings = db.Column(db.Float)
    annual_demand_savings = db.Column(db.Float)
    ad_budget_py = db.Column(db.Float)
    admin_budget_py_adjust = db.Column(db.Float)