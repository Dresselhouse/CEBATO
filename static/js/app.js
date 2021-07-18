const navbar = document.querySelector('.navbar')

const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.primary-nav');
    const navLinks = document.querySelectorAll('.primary-nav li')

    burger.addEventListener('click', () => {
        //toggle nav
        nav.classList.toggle('nav-active');

        //Navlinks animation
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = ''
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`;
            }

        });
        //Burger animation
        burger.classList.toggle('toggle');

    });

    //Close mobile nav with tap outside of it
    document.addEventListener('click', (e) => {
        if (nav.classList.contains('nav-active')) {            
            if (e.clientX < window.innerWidth * 0.5) {                

                nav.classList.toggle('nav-active')
                navLinks.forEach((link, index) => {
                    if (link.style.animation) {
                        link.style.animation = ''
                    } else {
                        link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`;
                    }

                });

                //Burger animation
                burger.classList.toggle('toggle');

            }
        }
    })
}

navSlide();