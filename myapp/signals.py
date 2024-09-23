from django.db.models.signals import post_save, post_delete, post_migrate
from django.dispatch import receiver
from .models import Article

@receiver(post_save, sender=Article)
def article_post_save(sender, instance, created, **kwargs):
    if created:
        print("New Article Created")
    else:
        print("Article Updated") 
        
@receiver(post_delete, sender=Article)
def article_post_delete(sender, instance, **kwargs):
        print("Article Deleted: ", instance)


import logging
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps
from django.db import connections
import os
from slack_sdk import WebClient

logging.basicConfig(filename='migrations_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Slack configuration
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL')

slack_client = WebClient(token=SLACK_TOKEN)

@receiver(post_migrate)
def log_migration(sender, **kwargs):
    app_name = sender.name

    # Ensure we only log for installed apps
    if app_name in apps.app_configs:
        # Get the applied migrations for the app
        connection = connections[kwargs.get('using', 'default')]
        cursor = connection.cursor()
        
        cursor.execute("SELECT name FROM django_migrations WHERE app = %s", [app_name])
        applied_migrations = [row[0] for row in cursor.fetchall()]

        # Log migration details
        if applied_migrations:
            logging.info(f"Migrations for '{app_name}':")
            for migration_name in applied_migrations:
                migration_file = f"{app_name}/migrations/{migration_name}.py"
                logging.info(f"  {migration_file}")

        logging.info(f'Migration applied for app: {app_name}')
