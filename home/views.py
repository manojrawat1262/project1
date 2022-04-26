from django.shortcuts import render
from .models import*
# Create your views here.
from django.views.generic import View

class BaseView(View):
	views = {}



class HomeView(BaseView):
	def get(self,request):
		self.views['categories'] = Category.objects.all()
		self.views['subcategories'] = SubCategory.objects.all()
		self.views['sliders'] = Slider.objects.all()
		self.views['ads'] = Ad.objects.all()
		self.views['products'] = Product.objects.filter(stock = 'In Stock')
		self.views['sale_products'] = Product.objects.filter(labels = 'sale',stock = 'In Stock')
		self.views['hot_products'] = Product.objects.filter(labels = 'hot',stock = 'In Stock')
		self.views['new_products'] = Product.objects.filter(labels = 'new',stock = 'In Stock')


		return render(request, 'shop-index.html',self.views)



class DetailView(BaseView):
	def get(self,request,slug):
		self.views['product_detail'] = Product.objects.filter(slug = slug)


		return render(request,'shop-item.html',self.views)




class CategoryView(BaseView):
	def get(self,request,slug):
		cat_id = Category.objects.get(slug = slug).id
		self.views['category_products'] = Product.objects.filter(category_id = cat_id)


		return render(request,'category.html',self.views)