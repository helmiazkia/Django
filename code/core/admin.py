# admin.py
from django.contrib import admin
from django import forms
from .models import Course, CourseContent, Comment, CourseMember

# Kelas Form untuk validasi tambahan
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Harga tidak boleh negatif!")
        return price

# Inline untuk CourseMember
class CourseMemberInline(admin.TabularInline):
    model = CourseMember
    extra = 1  # Jumlah baris kosong untuk penambahan data baru

# Admin untuk Course
class CourseAdmin(admin.ModelAdmin):
    form = CourseForm  # Menambahkan form khusus
    list_display = ('name', 'price', 'teacher', 'is_deleted')  # Menampilkan kolom tambahan
    list_filter = ('teacher', 'price', 'is_deleted')  # Filter berdasarkan kolom
    search_fields = ('name', 'teacher__username')  # Kolom yang bisa dicari
    actions = ['set_price_to_zero']  # Menambahkan aksi kustom
    inlines = [CourseMemberInline]  # Menambahkan inline untuk CourseMember

    def set_price_to_zero(self, request, queryset):
        queryset.update(price=0)
        self.message_user(request, "Harga berhasil diatur ke 0 untuk kursus yang dipilih.")
    set_price_to_zero.short_description = "Set harga ke 0 untuk kursus terpilih"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(is_deleted=False)  # Menyembunyikan data yang di-soft delete

    def delete_model(self, request, obj):
        obj.delete()  # Menggunakan soft delete alih-alih menghapus

# Mendaftarkan model ke admin
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseMember)
admin.site.register(CourseContent)
admin.site.register(Comment)

