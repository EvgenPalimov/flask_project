$(function () {
    let cur_url = document.location.pathname;
    $('.tm-nav li').each(function () {
        let link = $(this).find('a').attr('href');
        if (cur_url === link) {
            $(this).addClass('active');
        }
    });
});