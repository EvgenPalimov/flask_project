$(function () {
    var cur_url = '/'.pop();
    $('.tm-nav li').each(function () {
        var link = $(this).find('a').attr('href');
        if (cur_url === link) {
            $(this).addClass('active');
        }
    });
});