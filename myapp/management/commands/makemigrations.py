import logging
from django.core.management import CommandError
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from ...signals import makemigrations_signal

# Configure logger
logger = logging.getLogger(__name__)

class Command(MakemigrationsCommand):
    help = 'Run makemigrations and capture the output.'

    def handle(self, *args, **options):
        # Create a list to hold output
        output = []

        # Override the stdout.write method to capture output
        original_write = self.stdout.write

        def capture_output(msg, *args, **kwargs):
            output.append(msg)
            original_write(msg, *args, **kwargs)

        # Assign the new method to capture output
        self.stdout.write = capture_output

        try:
            # Call the original makemigrations command
            super().handle(*args, **options)
        except CommandError as e:
            logger.error("CommandError: %s", str(e))
            self.stderr.write(f"Error: {str(e)}")
            return
        finally:
            # Restore original stdout.write
            self.stdout.write = original_write

        # Join the captured output
        final_output = ''.join(output).strip()  # Get the captured output

        if final_output:
            # Send to Slack or other integrations
            makemigrations_signal.send(sender=self.__class__, output=final_output)
        else:
            self.stdout.write("No changes detected.")  # Fallback message if no output