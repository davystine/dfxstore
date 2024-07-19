from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models import Item, Category
from management.forms import ItemForm, CategoryForm
from django.contrib import messages
from .mixins import AdminRequiredMixin

# Item Views
class ItemListView(AdminRequiredMixin, View):
    def get(self, request):
        items = Item.objects.all()
        return render(request, 'management/item_list.html', {'items': items})

class ItemCreateView(AdminRequiredMixin, View):
    def get(self, request):
        form = ItemForm()
        return render(request, 'management/item_form.html', {'form': form})

    def post(self, request):
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item was successfully created.')
            return redirect('management:item_list')
        for error in form.errors.values():
            messages.error(request, error)
        return render(request, 'management/item_form.html', {'form': form})

class ItemUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        form = ItemForm(instance=item)
        return render(request, 'management/item_form.html', {'form': form})

    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item was successfully updated.')
            return redirect('management:item_list')
        for error in form.errors.values():
            messages.error(request, error)
        return render(request, 'management/item_form.html', {'form': form})

class ItemDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        item_name = item.name
        item.delete()
        messages.success(request, f'Item "{item_name}" was successfully deleted.')
        return redirect('management:item_list')

# Category Views
class CategoryListView(AdminRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'management/category_list.html', {'categories': categories})

class CategoryCreateView(AdminRequiredMixin, View):
    def get(self, request):
        form = CategoryForm()
        return render(request, 'management/category_form.html', {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category was successfully created.')
            return redirect('management:category_list')
        for error in form.errors.values():
            messages.error(request, error)
        return render(request, 'management/category_form.html', {'form': form})

class CategoryUpdateView(AdminRequiredMixin, View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(instance=category)
        return render(request, 'management/category_form.html', {'form': form})

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category was successfully updated.')
            return redirect('management:category_list')
        for error in form.errors.values():
            messages.error(request, error)
        return render(request, 'management/category_form.html', {'form': form})

class CategoryDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" was successfully deleted.')
        return redirect('management:category_list')
