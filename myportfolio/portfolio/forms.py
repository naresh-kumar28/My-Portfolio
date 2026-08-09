import re
from django import forms
from .models import Contact, Project, Skill, Certificate

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'contact', 'message']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_image', 'image_url', 'project_name', 'project_about', 'technology', 'project_url', 'github_url']

    def clean_project_image(self):
        image = self.cleaned_data.get('project_image')
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image size cannot exceed 5MB.")
        return image




class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'svg_code']

    def clean_svg_code(self):
        code = self.cleaned_data.get('svg_code', '').strip()
        if not code:
            return code

        # Disallow script, iframe, object, embed, form, link, style tags
        forbidden_tags = [r'<script', r'<iframe', r'<object', r'<embed', r'<form', r'<input', r'<link', r'<meta']
        for tag in forbidden_tags:
            if re.search(tag, code, re.IGNORECASE):
                raise forms.ValidationError("Input contains disallowed HTML/JS tags.")

        # Disallow dangerous event handlers (onload, onerror, onclick, etc.)
        if re.search(r'\bon[a-z]+\s*=', code, re.IGNORECASE):
            raise forms.ValidationError("Input contains dangerous event attributes (e.g. onload, onerror).")

        # Disallow javascript: pseudo-protocol
        if re.search(r'javascript\s*:', code, re.IGNORECASE):
            raise forms.ValidationError("Input contains dangerous javascript: URLs.")

        # Must contain standard icon markup (<i, <svg, <path, <span, <img)
        if not re.search(r'<(i|svg|path|g|circle|rect|polygon|polyline|line|span|img)\b', code, re.IGNORECASE):
            raise forms.ValidationError("Input must be valid icon HTML/SVG markup (e.g. <i> or <svg>).")

        return code


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['title', 'issuer', 'certificate_image', 'image_url', 'issue_date', 'credential_url']

    def clean_certificate_image(self):
        image = self.cleaned_data.get('certificate_image')
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Certificate image size cannot exceed 5MB.")
        return image
