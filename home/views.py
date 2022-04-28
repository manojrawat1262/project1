from django.shortcuts import render, redirect
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
		cat_name = Category.objects.get(slug = slug).name
		self.views['cat_name'] = cat_name
		self.views['subcategories'] = SubCategory.objects.filter(category_id = cat_id)
		self.views['category_products'] = Product.objects.filter(category_id = cat_id)

		return render(request,'category.html',self.views)



class SubCategoryView(BaseView):
	def get(self,request,slug):
		subcat_id = SubCategory.objects.get(slug = slug).id
		self.views['subcategory_products'] = Product.objects.filter(subcategory_id = subcat_id)

		return render(request,'subcategory.html',self.views)

from django.db.models import Q
class SearchView(BaseView):
	def get(self,request):
		if request.method == 'GET':
			query = request.GET['query']
			# self.views['search_products'] = Product.objects.filter((name_icontains = query) | (description_icontains = query))
			lookups= Q(name__icontains = query ) | Q(description__icontains = query ) 
			self.views['search_products'] = Product.objects.filter(lookups).distinct()
			self.views['search_for'] = query

		return render(request,'shop-search-result.html',self.views)

from django.contrib import messages
from django.contrib.auth.models import User

def signup(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		cpassword = request.POST['cpassword']


		if password == cpassword:
			if User.objects.filter(username = username).exists():
				message.error(request,'the username is already taken')
				return render(request,'shop-standart-forms.html')
			elif User.objects.filter(email = email).exists():
				message.error(request,'the email is already taken')
				return render(request,'shop-standart-forms.html')
				return redirect('/signup')

			else:
				user = User.objects.create_user(
					username = username,
					email = email,
					password = password

					)
				user.save()

		else:
				message.error(request,'the password does not match')
				return render(request,'shop-standart-forms.html')
		




	return render(request,'shop-standart-forms.html')