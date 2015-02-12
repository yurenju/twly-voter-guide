# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django.utils import timezone
from json_field import JSONField
from vote.models import Vote, Legislator_Vote
from bill.models import Legislator_Bill
from committees.models import Legislator_Committees


class Attendance(models.Model):
    legislator = models.ForeignKey('legislator.LegislatorDetail')
    sitting = models.ForeignKey('sittings.Sittings', to_field="uid")
    category = models.CharField(db_index=True, max_length=100)
    status = models.CharField(db_index=True, max_length=100)
    def __unicode__(self):
        return self.sitting

class Legislator(models.Model):
    uid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    former_names = models.CharField(max_length=100, blank=True, null=True)
    def __unicode__(self):
        return self.name

class LegislatorDetail(models.Model):
    legislator = models.ForeignKey(Legislator, to_field="uid", related_name='each_terms')
    ad = models.IntegerField(db_index=True, )
    name = models.CharField(db_index=True, max_length=100)
    gender = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    party = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    caucus = models.CharField(max_length=100, blank=True, null=True)
    constituency = models.IntegerField(db_index=True, blank=True, null=True)
    county = models.CharField(db_index=True, max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    in_office = models.BooleanField(db_index=True, )
    contacts = JSONField(null=True)
    term_start = models.DateField(blank=True, null=True)
    term_end = JSONField(null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    remark = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    links = JSONField(null=True)
    platform = models.TextField(blank=True, null=True)
    bill_param = JSONField(null=True)
    vote_param = JSONField(null=True)
    attendance_param = JSONField(null=True)

    class Meta:
        unique_together = ("legislator", "ad")

    def __unicode__(self):
        return self.name

    def _in_office_ad(self):
        return LegislatorDetail.objects.filter(legislator_id=self.legislator_id).values_list('ad', flat=True).order_by('-ad')
    in_office_ad = property(_in_office_ad)

    def _not_vote_percentage(self):
        if Legislator_Vote.objects.filter(legislator_id=self.id):
            return Legislator_Vote.objects.filter(decision__isnull=True, legislator_id=self.id).count() * 100.0 / Legislator_Vote.objects.filter(legislator_id=self.id).count()
        return 0
    pnotvote = property(_not_vote_percentage)

    def _not_vote_count(self):
        return Legislator_Vote.objects.filter(decision__isnull=True, legislator_id=self.id).count()
    notvote = property(_not_vote_count)

    def _conscience_vote_percentage(self):
        if Vote.objects.filter(sitting__ad=self.ad):
            return Legislator_Vote.objects.filter(legislator_id=self.id, conflict=True).count() * 100.0 / Vote.objects.filter(sitting__ad=self.ad).count()
    pconsciencevote = property(_conscience_vote_percentage)

    def _conscience_vote_count(self):
        return Legislator_Vote.objects.filter(legislator_id=self.id, conflict=True).count()
    nconsciencevote = property(_conscience_vote_count)

    def _pribiller_count(self):
        return Legislator_Bill.objects.filter(legislator_id=self.id, priproposer=True).count()
    npribill = property(_pribiller_count)

    def _current_committee(self):
        committees = Legislator_Committees.objects.filter(legislator_id=self.id).order_by('-session')
        if committees:
            return committees[0].committee
    current_committee = property(_current_committee)

    def _ly_absent_count(self):
        return Attendance.objects.filter(legislator_id=self.id, category='YS', status='absent').count()
    ly_absent = property(_ly_absent_count)

class FileLog(models.Model):
    sitting = models.CharField(unique=True, max_length=100)
    date = models.DateTimeField()
    def __unicode__(self):
        return self.session
