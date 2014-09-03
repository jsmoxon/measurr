# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'pg_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'pg', ['UserProfile'])

        # Adding model 'Manager'
        db.create_table(u'pg_manager', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_profile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pg.UserProfile'])),
            ('is_manager', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pg', ['Manager'])

        # Adding model 'PriorityQuestion'
        db.create_table(u'pg_priorityquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pg', ['PriorityQuestion'])

        # Adding model 'PriorityChoice'
        db.create_table(u'pg_prioritychoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('priority_question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pg.PriorityQuestion'])),
            ('choice_text', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('choice_value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'pg', ['PriorityChoice'])

        # Adding model 'Project'
        db.create_table(u'pg_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pg.Manager'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pg', ['Project'])

        # Adding M2M table for field workers on 'Project'
        m2m_table_name = db.shorten_name(u'pg_project_workers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'pg.project'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'pg.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'userprofile_id'])

        # Adding M2M table for field questions on 'Project'
        m2m_table_name = db.shorten_name(u'pg_project_questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'pg.project'], null=False)),
            ('priorityquestion', models.ForeignKey(orm[u'pg.priorityquestion'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'priorityquestion_id'])

        # Adding model 'TaskRating'
        db.create_table(u'pg_taskrating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('long_review', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pg', ['TaskRating'])

        # Adding model 'Task'
        db.create_table(u'pg_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pg.Project'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('primary_assignee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pg.UserProfile'])),
            ('priority_rank', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('future_eval_interval', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_completed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'pg', ['Task'])

        # Adding M2M table for field task_rating on 'Task'
        m2m_table_name = db.shorten_name(u'pg_task_task_rating')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm[u'pg.task'], null=False)),
            ('taskrating', models.ForeignKey(orm[u'pg.taskrating'], null=False))
        ))
        db.create_unique(m2m_table_name, ['task_id', 'taskrating_id'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'pg_userprofile')

        # Deleting model 'Manager'
        db.delete_table(u'pg_manager')

        # Deleting model 'PriorityQuestion'
        db.delete_table(u'pg_priorityquestion')

        # Deleting model 'PriorityChoice'
        db.delete_table(u'pg_prioritychoice')

        # Deleting model 'Project'
        db.delete_table(u'pg_project')

        # Removing M2M table for field workers on 'Project'
        db.delete_table(db.shorten_name(u'pg_project_workers'))

        # Removing M2M table for field questions on 'Project'
        db.delete_table(db.shorten_name(u'pg_project_questions'))

        # Deleting model 'TaskRating'
        db.delete_table(u'pg_taskrating')

        # Deleting model 'Task'
        db.delete_table(u'pg_task')

        # Removing M2M table for field task_rating on 'Task'
        db.delete_table(db.shorten_name(u'pg_task_task_rating'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'pg.manager': {
            'Meta': {'object_name': 'Manager'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_manager': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'user_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pg.UserProfile']"})
        },
        u'pg.prioritychoice': {
            'Meta': {'object_name': 'PriorityChoice'},
            'choice_text': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'choice_value': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority_question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pg.PriorityQuestion']"})
        },
        u'pg.priorityquestion': {
            'Meta': {'object_name': 'PriorityQuestion'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'})
        },
        u'pg.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pg.Manager']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pg.PriorityQuestion']", 'symmetrical': 'False'}),
            'workers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pg.UserProfile']", 'symmetrical': 'False'})
        },
        u'pg.task': {
            'Meta': {'object_name': 'Task'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'future_eval_interval': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'primary_assignee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pg.UserProfile']"}),
            'priority_rank': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pg.Project']"}),
            'task_rating': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['pg.TaskRating']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'pg.taskrating': {
            'Meta': {'object_name': 'TaskRating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_review': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'pg.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['pg']