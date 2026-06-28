from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import os
import re

def validate_email(value):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, value):
        raise ValidationError('Enter a valid email address.')
    return value

@deconstructible
class FileTypeValidator:
    """Validator to check uploaded file types"""
    
    def __init__(self, allowed_types=None, max_size_mb=500):
        self.allowed_types = allowed_types or [
            'application/pdf',
            'application/epub+zip',
            'application/mobi',
            'application/zip',
            'video/mp4',
            'audio/mpeg',
            'application/x-rar-compressed',
        ]
        self.max_size_mb = max_size_mb
        self.max_size_bytes = max_size_mb * 1024 * 1024
    
    def __call__(self, file):
        # Check file size
        if file.size > self.max_size_bytes:
            raise ValidationError(
                f'File size must be less than {self.max_size_mb}MB. '
                f'Current size: {file.size / (1024*1024):.2f}MB'
            )
        
        # Check file type
        if hasattr(file, 'content_type'):
            if file.content_type not in self.allowed_types:
                raise ValidationError(
                    f'Invalid file type. Allowed types: {", ".join(self.allowed_types)}'
                )
        
        # Check file extension as backup
        ext = os.path.splitext(file.name)[1].lower()
        allowed_extensions = ['.pdf', '.epub', '.mobi', '.zip', '.mp4', '.mp3', '.rar']
        if ext not in allowed_extensions:
            raise ValidationError(
                f'Invalid file extension. Allowed extensions: {", ".join(allowed_extensions)}'
            )


@deconstructible
class ImageURLValidator:
    """Validator for image URLs"""
    
    def __call__(self, url):
        if not url:
            return
        
        # Check if it's a valid URL
        from urllib.parse import urlparse
        parsed = urlparse(url)
        
        if not all([parsed.scheme, parsed.netloc]):
            raise ValidationError('Enter a valid URL.')
        
        # Check if it's an image URL (basic check)
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
        path_lower = parsed.path.lower()
        
        # Allow URLs without extensions (like TMDB URLs)
        if not any(path_lower.endswith(ext) for ext in image_extensions):
            # Check if it looks like an image service
            if 'tmdb' not in url and 'openlibrary' not in url:
                raise ValidationError('URL does not appear to be an image.')