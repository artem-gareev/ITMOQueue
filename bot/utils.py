from database import crud
from view import messages


def get_queue_text(subject_id, practice_id, persons, user_id):
    subject = crud.get_subject(subject_id)
    practice = crud.get_practice(practice_id)

    text = messages.QUEUE_HEADER.format(practice=practice.name, subject=subject.name)

    for i, person in enumerate(persons):
        user = crud.get_user(person.user_id)
        if person == user_id:
            text += f"\n<b>{i + 1}.({'N' if person.is_new else 'Q'}) {user.name}</b>"
        else:
            text += f"\n{i + 1}.({'N' if person.is_new else 'Q'}){user.name}"

    if not persons:
        text += messages.NO_PERSONS
    return text
