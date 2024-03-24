from flask import jsonify
from sqlalchemy import create_engine, String, select, or_, delete, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy_utils import create_database, database_exists

engine = create_engine('mysql+pymysql://root:1234@127.0.0.1/phonebook')


class Base(DeclarativeBase):
    pass


class Contacts(Base):
    __tablename__ = 'contacts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'phone': self.phone
        }

    @classmethod
    def get(cls, term):
        with Session(engine) as session:
            stmt = select(Contacts).filter(or_(Contacts.name.contains(term),
                                               Contacts.surname.contains(term),
                                               Contacts.phone.contains(term)))

            contacts = [contact.serialize for contact in session.scalars(stmt)]

        return {'data': contacts}

    @classmethod
    def post(cls, contact):
        with Session(engine) as session:
            if session.scalar(select(Contacts).filter_by(phone=contact['phone'])):
                return jsonify({'success': False, 'message': 'Номер телефона должен быть уникальным'}), 200

            session.add(Contacts(name=contact['name'], surname=contact['surname'], phone=contact['phone']))
            session.commit()

        return jsonify({'success': True, 'message': ''}), 200

    @classmethod
    def delete(cls, contacts_ids):
        with Session(engine) as session:
            session.execute(delete(Contacts).where(Contacts.id.in_(contacts_ids)))
            session.commit()

        return jsonify({'success': True, 'message': ''}), 200

    @classmethod
    def put(cls, saved_contact):
        with Session(engine) as session:
            if session.scalar(select(Contacts).filter(Contacts.id != saved_contact['id'])
                                              .filter(Contacts.phone == saved_contact['phone'])):
                return jsonify({'data': {'success': False, 'message': 'Номер телефона должен быть уникальным'}}), 200

            stmt = update(Contacts).where(Contacts.id == saved_contact['id']).values(name=saved_contact['name'],
                                                                                     surname=saved_contact['surname'],
                                                                                     phone=saved_contact['phone'])
            session.execute(stmt)
            session.commit()

        return jsonify({'data': {'success': True, 'message': ''}}), 200

    def __repr__(self):
        return '{id: %s, name: %s, surname: %s, phone: %s}' % (self.id, self.name, self.surname, self.phone)


if not database_exists(engine.url):
    create_database(engine.url)
    Base.metadata.create_all(engine)
