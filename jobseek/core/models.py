"""Models for the jobseek app."""
from django.db import models


class BaseModel(models.Model):
    """Base model for all models."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True


class JobStatus(models.TextChoices):
    """Statuses for the job model."""
    APPLIED = 'Резюме отправлено'
    INTERVIEWING = 'В процессе собеседований'
    OFFER = 'Оффер'
    REJECTED = 'Отказ'
    NOT_INTERESTED = 'Не интересно'


class InterviewType(models.TextChoices):
    """Types of interviews."""
    SCREENING = 'Скрининг'
    TECHNICAL = 'Техническое интервью'
    TECHNICAL_FOLLOW_UP = 'ОС по результатам технического интервью'
    HR = 'HR-интервью'
    HR_FOLLOW_UP = 'ОС по результатам HR-интервью'
    OFFER = 'Оффер'


class InterviewStatus(models.TextChoices):
    """Statuses for the interview model."""
    PASSED = 'Пройден'
    FAILED = 'Не пройден'
    NOT_TAKEN = 'Не проходил'


class Interview(BaseModel):
    """Interview model."""
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    type = models.CharField(max_length=255, choices=InterviewType.choices)
    status = models.CharField(max_length=255, choices=InterviewStatus.choices)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.job.title} - {self.type} - {self.status} - {self.date}"

    class Meta:
        ordering = ['-date']
        verbose_name = 'Interview'
        verbose_name_plural = 'Interviews'


class Company(BaseModel):
    """Company model."""
    name = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Recruiter(BaseModel):
    """Recruiter model."""
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Recruiter'
        verbose_name_plural = 'Recruiters'


class Job(BaseModel):
    """Job model."""
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(max_length=255)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    history = models.ManyToManyField('JobHistory', related_name='jobs')
    status = models.CharField(
        max_length=255, choices=JobStatus.choices, default=JobStatus.APPLIED)
    interviews = models.ManyToManyField('Interview', related_name='jobs')

    def add_history(self, status, date):
        history = JobHistory(job=self, status=status, date=date)
        history.save()
        self.history.add(history)
        self.save()

    def __str__(self):
        return self.title + ' - ' + self.company.name

    class Meta:
        ordering = ['-history__date']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'


class JobHistory(BaseModel):
    """Job history model."""
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=JobStatus.choices)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.job.title} - {self.status} - {self.date}"

    class Meta:
        ordering = ['-date']
        verbose_name = 'Job history'
        verbose_name_plural = 'Job histories'
