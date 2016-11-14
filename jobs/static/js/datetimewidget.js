jQuery(document).ready(function () {
    'use strict';
    jQuery.datetimepicker.setLocale("ru");
    jQuery(".DateTimeWidget").datetimepicker({
        format: 'd.m.Y H:i',
        dayOfWeekStart: 1,
        step: 5,
    });
    jQuery(".DateWidget").datetimepicker({
        format: 'd.m.Y',
        timepicker: false,
        dayOfWeekStart: 1,
    });
    jQuery(".TimeWidget").datetimepicker({
        format: 'H:i',
        timepicker: true,
        datepicker: false,
        // dayOfWeekStart: 1,
        step: 5,
    });
});
