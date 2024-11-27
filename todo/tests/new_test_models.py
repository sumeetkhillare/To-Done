from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from todo.models import List, ListTags, ListItem, Template, TemplateItem, SharedUsers, SharedList, Task, VoiceNote
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass')
        self.list = List.objects.create(
            title_text="Test List",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        self.list_item = ListItem.objects.create(
            item_text="Test Item",
            created_on=timezone.now(),
            list=self.list,
            finished_on=timezone.now(),
            due_date=timezone.now().date(),
            tag_color="red"
        )

    def test_list_creation(self):
        self.assertTrue(isinstance(self.list, List))
        self.assertEqual(str(self.list), "Test List")

    def test_list_tags_creation(self):
        list_tag = ListTags.objects.create(
            user_id=self.user,
            tag_name="Important",
            created_on=timezone.now()
        )
        self.assertTrue(isinstance(list_tag, ListTags))
        self.assertEqual(str(list_tag), "Important")

    def test_list_item_creation(self):
        self.assertTrue(isinstance(self.list_item, ListItem))
        self.assertEqual(str(self.list_item), "Test Item: False")

    def test_template_creation(self):
        template = Template.objects.create(
            title_text="Test Template",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        self.assertTrue(isinstance(template, Template))
        self.assertEqual(str(template), "Test Template")

    def test_template_item_creation(self):
        template = Template.objects.create(
            title_text="Test Template",
            created_on=timezone.now(),
            updated_on=timezone.now(),
            user_id=self.user
        )
        template_item = TemplateItem.objects.create(
            item_text="Test Template Item",
            created_on=timezone.now(),
            template=template,
            finished_on=timezone.now(),
            due_date=timezone.now().date(),
            tag_color="blue"
        )
        self.assertTrue(isinstance(template_item, TemplateItem))
        self.assertEqual(str(template_item), "Test Template Item")

    def test_shared_users_creation(self):
        shared_user = SharedUsers.objects.create(
            list_id=self.list,
            shared_user="shareduser@example.com"
        )
        self.assertTrue(isinstance(shared_user, SharedUsers))
        self.assertEqual(str(shared_user), str(self.list))

    def test_shared_list_creation(self):
        shared_list = SharedList.objects.create(
            user=self.user,
            shared_list_id="shared_list_1"
        )
        self.assertTrue(isinstance(shared_list, SharedList))
        self.assertEqual(str(shared_list), str(self.user))

    def test_task_creation(self):
        task = Task.objects.create(
            title="Test Task",
            status="todo",
            user=self.user
        )
        self.assertTrue(isinstance(task, Task))
        self.assertEqual(str(task), "Test Task")

    def test_voice_note_creation(self):
        voice_note = VoiceNote.objects.create(
            user=self.user,
            audio_file="path/to/audio.mp3",
            list_item=self.list_item
        )
        self.assertTrue(isinstance(voice_note, VoiceNote))
        self.assertEqual(str(voice_note), f"Voice Note for {self.list_item.item_name}")

    def test_list_is_shared_default(self):
        self.assertFalse(self.list.is_shared)

    def test_list_item_is_done_default(self):
        self.assertFalse(self.list_item.is_done)

    def test_task_status_choices(self):
        task = Task.objects.create(
            title="Test Task",
            status="in_progress",
            user=self.user
        )
        self.assertEqual(task.status, "in_progress")

    def test_list_item_status_null(self):
        list_item = ListItem.objects.create(
            item_text="Test Item",
            created_on=timezone.now(),
            list=self.list,
            finished_on=timezone.now(),
            due_date=timezone.now().date(),
            tag_color="red"
        )
        self.assertIsNone(list_item.status)

    def test_template_user_null(self):
        template = Template.objects.create(
            title_text="Test Template",
            created_on=timezone.now(),
            updated_on=timezone.now()
        )
        self.assertIsNone(template.user_id)

    def test_voice_note_related_name(self):
        voice_note = VoiceNote.objects.create(
            user=self.user,
            audio_file="path/to/audio.mp3",
            list_item=self.list_item
        )
        self.assertIn(voice_note, self.list_item.voice_notes.all())

    def test_voice_note_related(self):
        voice_note = VoiceNote.objects.create(
            user=self.user,
            audio_file="path/to/audio.mp3",
            list_item=self.list_item
        )
        self.assertIn(voice_note, self.list_item.voice_notes.all())

    def test_list_cascade_delete(self):
        list_id = self.list.id
        self.user.delete()
        with self.assertRaises(List.DoesNotExist):
            List.objects.get(id=list_id)

    def test_task_status_default(self):
        task = Task.objects.create(
            title="Test Task",
            user=self.user
        )
        self.assertEqual(task.status, "todo")

    def test_voice_note_auto_now_add(self):
        voice_note = VoiceNote.objects.create(
            user=self.user,
            audio_file="path/to/audio.mp3",
            list_item=self.list_item
        )
        self.assertIsNotNone(voice_note.created_at)

    def test_voice_note_auto(self):
        voice_note = VoiceNote.objects.create(
            user=self.user,
            audio_file="path/to/audio2.mp3",
            list_item=self.list_item
        )
        self.assertIsNotNone(voice_note.created_at)