from django import forms


class SimpleExcelUploadForm(forms.Form):
    """简单的Excel上传表单"""
    excel_file = forms.FileField(
        label='Excel文件',
        help_text='请选择包含地标数据的Excel文件（.xlsx格式），第一行必须是表头',
        widget=forms.FileInput(attrs={
            'accept': '.xlsx,.xls',
            'class': 'form-control'
        })
    )
    
    def clean_excel_file(self):
        """验证Excel文件"""
        file = self.cleaned_data.get('excel_file')
        if file:
            # 检查文件大小（限制为10MB）
            if file.size > 100 * 1024 * 1024:
                raise forms.ValidationError('文件大小不能超过100MB')
            
            # 检查文件扩展名
            allowed_extensions = ['.xlsx', '.xls']
            file_extension = file.name.lower()
            if not any(file_extension.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError('只支持.xlsx和.xls格式的文件')
        
        return file 