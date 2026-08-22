from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from accounts.models import User, Profile
from blog.models import Post, Category


class Command(BaseCommand):
    help = "inserting fake data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, default=5)
        parser.add_argument("--categories", type=int, default=3)
        parser.add_argument("--posts", type=int, default=10)

    def handle(self, *args, **options):
        # ساخت کاربران و پروفایل‌ها
        profiles = []
        for _ in range(options["users"]):
            user = User.objects.create_user(
                email=self.fake.email(), password="Qazx3erfff@"
            )
            profile = Profile.objects.get(user=user)
            profile.first_name = self.fake.first_name()
            profile.last_name = self.fake.last_name()
            profile.bio = self.fake.paragraph(nb_sentences=4)
            profile.save()
            profiles.append(profile)

        # ساخت کتگوری‌ها
        categories = []
        for _ in range(options["categories"]):
            category = Category.objects.create(name=self.fake.word().title())
            categories.append(category)

        # ساخت پست‌ها
        for _ in range(options["posts"]):
            Post.objects.create(
                author=self.fake.random_element(profiles),
                title=self.fake.sentence(nb_words=6),
                content=self.fake.paragraph(nb_sentences=10),
                status=True,
                category=self.fake.random_element(categories),
                published_date=timezone.now(),
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Inserted {options['users']} users, "
                f"{options['categories']} categories, "
                f"{options['posts']} posts."
            )
        )
