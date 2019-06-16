from django.shortcuts import render, redirect
from contacts.models import Contact
from django.contrib import messages
from django.core.mail import send_mail


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listin_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'Bu ev için oluşturulmuş bir mesajınız bulunmaktadır.')
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing, listin_id=listing_id, name=name, email=email, phone=phone,message=message, user_id=user_id)
        contact.save()

        # Send mail
        send_mail(
            'Emlak Sorunuz',
            listing + ' sorusu sorulmuştur. Detay için admin panalini kontrol ediniz.',
            'uzemyazilim@gmail.com',
            [
                realtor_email,
                'tatukaci@gmail.com'
            ],
            fail_silently=False
        )

        messages.success(request, 'Mesajınız başarı ile iletilmiştir.')
        return redirect('/listings/'+listing_id)



