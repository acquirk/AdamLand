from app import db, app
from app.models import Bucket

def init_db():
    with app.app_context():
        db.create_all()
        
        # Check if buckets already exist
        if Bucket.query.count() == 0:
            buckets = [
                Bucket(name='Internal', subtitle='Nurture your inner self', advice='Self-improvement is a lifelong journey.'),
                Bucket(name='Home', subtitle='Create your sanctuary', advice='A well-organized home leads to a peaceful mind.'),
                Bucket(name='Family', subtitle='Cherish your relationships', advice='Strong bonds are built on communication and shared experiences.'),
                Bucket(name='External', subtitle='Share your gifts with the world', advice='Your unique perspective can make a difference.')
            ]
            db.session.add_all(buckets)
            db.session.commit()
            print("Database initialized with default buckets.")
        else:
            print("Database already contains buckets.")
        
        # Create Archive bucket if it doesn't exist
        archive_bucket = Bucket.query.filter_by(name="Archive").first()
        if not archive_bucket:
            archive_bucket = Bucket(name="Archive", subtitle="Archived items", advice="Items moved here are no longer active but preserved for reference.")
            db.session.add(archive_bucket)
            db.session.commit()
            print("Archive bucket created.")

if __name__ == '__main__':
    init_db()
