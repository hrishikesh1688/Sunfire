odoo.define('eway_bill.DocumentViewer1', function (require) {
    "use strict";
    
    var core = require('web.core');
    var Widget = require('web.Widget');
    
    var QWeb = core.qweb;
    
    var SCROLL_ZOOM_STEP = 0.1;
    var ZOOM_STEP = 0.5;
    
    var DocumentViewer = Widget.extend({
        //template: "DocumentViewer1",
        events: {
            'click .o_download_btn': '_onDownload',
            'click .o_viewer_img': '_onImageClicked',
            'click .o_viewer_video': '_onVideoClicked',
            'click .move_next': '_onNext',
            'click .move_previous': '_onPrevious',
            'click .o_rotate': '_onRotate',
            'click .o_zoom_in': '_onZoomIn',
            'click .o_zoom_out': '_onZoomOut',
            'click .o_close_btn, .o_viewer_img_wrapper': '_onClose',
            'click .o_print_btn': '_onPrint',
            'DOMMouseScroll .o_viewer_content': '_onScroll',    // Firefox
            'mousewheel .o_viewer_content': '_onScroll',        // Chrome, Safari, IE
            'keydown': '_onKeydown',
            'keyup': '_onKeyUp',
            'mousedown .o_viewer_img': '_onStartDrag',
            'mousemove .o_viewer_content': '_onDrag',
            'mouseup .o_viewer_content': '_onEndDrag'
        },
        /**
         * The documentViewer takes an array of objects describing attachments in
         * argument, and the ID of an active attachment (the one to display first).
         * Documents that are not of type image or video are filtered out.
         *
         * @override
         * @param {Array<Object>} attachments list of attachments
         * @param {integer} activeAttachmentID
         */
        
        _onDownload: function (e) {
            // e.preventDefault();
            alert('OK')
            window.location = '/home/sai16/odoo-11.0/custom_addons/eway_bill/download/data.json?download=true';
        },
       
    });
    return DocumentViewer;
    });
    