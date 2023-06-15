let menu = document.querySelector("#menu-btn");
let navbar = document.querySelector('.header .navbar');
let loginForm = document.querySelector('.login-form');

document.querySelector('#login-btn').onclick = () => {
    loginForm.classList.toggle('active');
    navbar.classList.remove('active');
}
menu.onclick = () => {
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

window.onscroll = () => {

    menu.classList.remove('fa-times');
    navbar.classList.remove('active');

    if (window.scrollY > 60) {
        document.querySelector('#scroll-top').classList.add('active');
    } else {
        document.querySelector('#scroll-top').classList.remove('active');
    }

    if (window.scrollY > 60) {
        document.querySelector('.header').classList.add('active');
    }
    else {
        document.querySelector('.header').classList.remove('active');
    }

}

$(document).ready(function () {

    $(window).on('scroll load', function () {

        $('section').each(function () {

            let top = $(window).scrollTop();
            let height = $(this).height();
            let offset = $(this).offset().top - 200;
            let id = $(this).attr('id');

            if (top >= offset && top < offset + height) {
                $('.navbar a').removeClass('active');
                $('.navbar').find(`[href="#${id}"]`).addClass('active');
            }

        });

    });

});

var swiper = new Swiper(".team-slider", {
    loop: true,
    grabCursor: true,
    spaceBetween: 20,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    breakpoints: {
        0: {
            slidesPerView: 1,
        },
        768: {
            slidesPerView: 2,
        },
        991: {
            slidesPerView: 3,
        },
    },
});


// Dapatkan referensi ke elemen field menggunakan ID
var FirstName = document.getElementById("FirstName");
var LastName = document.getElementById("LastName");
var Email = document.getElementById("Email");
var PhoneNumber = document.getElementById("PhoneNumber");
var QuestionMessage = document.getElementById("QuestionMessage");

// Tambahkan event listener ke tombol submit
var submitButton = document.getElementById("submit");
submitButton.addEventListener("click", function (event) {
    event.preventDefault();

    var FirstName = document.getElementById("FirstName").value;
    var LastName = document.getElementById("LastName").value;
    var Email = document.getElementById("Email").value;
    var PhoneNumber = document.getElementById("PhoneNumber").value;
    var QuestionMessage = document.getElementById("QuestionMessage").value;

    // Simpan data ke Firestore
    db.collection("users").add({
        FirstName: FirstName,
        LastName: LastName,
        Email: Email,
        PhoneNumber: PhoneNumber,
        QuestionMessage: QuestionMessage
    })
        .then(function (docRef) {
            console.log("Data berhasil disimpan dengan ID:", docRef.id);
            // Tambahkan kode untuk menampilkan notifikasi di sini
        })
        .catch(function (error) {
            console.error("Error saat menyimpan data:", error);
        });
});



// Reset form setelah submit
document.getElementById("contactForm").reset();

// Tangani pengiriman form
var db = firebase.firestore();
var form = document.getElementById("contactForm");
form.addEventListener("submit", function (event) {
    event.preventDefault(); // Mencegah submit form mengarah ke halaman baru
    var FirstName = document.getElementById("FirstName").value;
    var LastName = document.getElementById("LastName").value;
    var Email = document.getElementById("Email").value;
    var PhoneNumber = document.getElementById("PhoneNumber").value;
    var QuestionMessage = document.getElementById("QuestionMessage").value;

    // Simpan data ke Firestore
    db.collection("ContactCustomer").add({
        FirstName: FirstName,
        LastName: LastName,
        Email: Email,
        PhoneNumber: PhoneNumber,
        QuestionMessage: QuestionMessage
    })
        .then(function (docRef) {
            console.log('Document written with ID: ', docRef.id);
            // Lakukan tindakan setelah pengiriman berhasil
        })
        .catch(function (error) {
            console.error('Error adding document: ', error);
            // Lakukan tindakan jika terjadi kesalahan
        });
});

// Meminta izin notifikasi saat halaman dimuat
window.addEventListener('load', function () {
    if ('Notification' in window) {
        Notification.requestPermission().then(function (permission) {
            if (permission === 'granted') {
                console.log('Izin notifikasi diberikan');
            }
        });
    }
});
