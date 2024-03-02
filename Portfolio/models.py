from django.db import models


# class Project(models.Model):
#     srno=models.IntegerField()
#     title=models.CharField(max_length=200)
#     client=models.CharField(max_length=200,null=True,blank=True)
#     short_description=models.TextField(null=True,blank=True)
#     description=models.TextField(null=True,blank=True)
#     vlink=models.CharField(max_length=200,null=True,blank=True)
#     glink=models.CharField(max_length=200,null=True,blank=True)
#     pic = models.ImageField(default="blank.png", null=True, blank=True)
    
    
#     def __str__(self):
#         return f'{self.title}'

class Project(models.Model):
    srno = models.IntegerField()
    title = models.CharField(max_length=200)
    client = models.CharField(max_length=200, null=True, blank=True)
    short_description = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    vlink = models.CharField(max_length=200, null=True, blank=True)
    glink = models.CharField(max_length=200, null=True, blank=True)
    pic = models.ImageField(default="blank.png", null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        # Check if the serial number is already in use
        if Project.objects.filter(srno=self.srno).exists():
            # Increment the serial number of existing projects with equal or greater numbers
            existing_projects = Project.objects.filter(srno__gte=self.srno)
            for project in existing_projects:
                project.srno += 1
                project.save()
        super(Project, self).save(*args, **kwargs)

class Certifications(models.Model):
    category=(
    ('programming','programming'),
    ('cloud','cloud'),
    ('networking','networking'),
    ('other','other'),
    )
    srno=models.IntegerField()
    title=models.CharField(max_length=200)
    filter=models.CharField(max_length=200,choices=category)
    pic = models.ImageField(default="blank.png", null=True, blank=True)
    
    
    def __str__(self):
        return f'{self.title}'



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100,)
    message = models.TextField(max_length=1000, default="")


    def __str__(self):
        return f'{self.name}'

class Resume(models.Model):
     resume_image = models.ImageField( null=True, blank=True)
     resume_pdf = models.FileField( null=True, blank=True)
     