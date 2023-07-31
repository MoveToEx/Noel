var quill = new Quill('.editor', {
    modules: {
        toolbar: {
            container: '#quill-toolbar'
        }
    },
    theme: 'snow',
    placeholder: '阿巴阿巴（°∀。）...\n不要从外部直接拖入图片哦，点击上方图片标志选择图片'
});


$('.mention-button').click(e => {
    let value = prompt('输入要提及的用户名');
    let index = 0;

    if (value === null) {
        return;
    }
    if (quill.getSelection()) {
        index = quill.getSelection().index;
    }
    else {
        index = quill.getLength();
    }

    quill.updateContents(new Delta().retain(index).insert({
        'mention': value
    }), Quill.sources.USER);

    quill.setSelection(index + 1, 0);
});

$('insert-ncm-button').click(e => {
    let s = $('#insert-ncm-input').val();
    let value, index;

    if (s == '') {
        return;
    }
    if (quill.getSelection()) {
        index = quill.getSelection().index;
    }
    else {
        index = quill.getLength();
    }

    if (/^\d+$/.test(value)) {
        value = s;
    }
    else if (s.match(/https:\/\/music\.163\.com\/(#\/)?song\?id=\d+(&userid=\d+)?/)) {
        value = s.match(/song\?id=(\d+)/)[1];
    }
    else {
        mdui.snackbar('未知的ID或链接格式');
        return;
    }

    quill.updateContents(new Delta().retain(index).insert({
        'ncm': value
    }), Quill.sources.USER);

    quill.setSelection(index + 1, 0);

});

var font_sizes = {
    "normal": "1.0em",
    "small": "0.75em",
    "large": "1.5em",
    "huge": "2.5em"
};

function validateImage(src) {
    if (src.startsWith('file:///')) {
        return false;
    }
    else if (src.startsWith('data:image/') && src.indexOf('base64') != -1) {
        return true;
    }
    else {
        return false;
    }
}

class Message {
    constructor() {
        this.messageContainer = $('<div class="mdui-row message-content mdui-col-offset-xs-1" />');
        this.headerContainer = $('<div class="mdui-row message-header" />');
    }

    setSender(sender) {
        if (sender.avatar) {
            $(`<img></img>`, {
                "class": "message-avatar",
                "source-user": sender.username,
                "src": sender.avatar
            }).dblclick(e => {
                let sel = quill.getSelection();
                if (sel) {
                    quill.updateContents(new Delta().retain(sel.index).insert({
                        'mention': e.target.getAttribute('source-user')
                    }), 'user');
                    quill.setSelection(sel.index + 1);
                }
                else {
                    quill.updateContents(new Delta().retain(quill.getLength() - 1).insert({
                        'mention': e.target.getAttribute('source-user')
                    }), 'user');
                    quill.setSelection(quill.getLength() - 1);
                }
            }).appendTo(this.headerContainer)
                .wrap($('<div class="mdui-col-md-1 mdui-col-xs-2"></div>'));
        }
        let col = $('<div class="mdui-col-md-11 mdui-col-xs-10 mdui-valign" />');
        if (sender.nickname) {
            $('<span class="message-nickname" />').text(sender.nickname).appendTo(col);
        }
        if (sender.username) {
            $('<span class="message-username" />').text('@' + sender.username).appendTo(col);
        }
        if (sender.title) {
            $(`<span class="user-title user-title-style-${sender.title_style}" />`).text(sender.title).appendTo(col);
        }
        col.appendTo(this.headerContainer);
    }

    appendText(text, attr) {
        let q = $('<span />').text(text).appendTo(this.messageContainer);
        if (attr) {
            if (attr.bold) q.wrap('<b />');
            if (attr.underline) q.wrap('<u />');
            if (attr.italic) q.wrap('<i />');
            if (attr.link) q.wrap(`<a href="${attr.link}" />`);
            if (attr.strike) q.wrap('<s />');
            if (attr.size) q.css('font-size', font_sizes[attr.size]);
        }
    }

    appendMention(text) {
        $(`<span class="mention">@${text}</span>`)
            .appendTo(this.messageContainer)
            .filter(x => text == sender.data.username)
            .addClass('mention-hit');
    }

    appendImage(src) {
        $(`<img src="${src}" />`).appendTo(this.messageContainer);
    }

    appendNCM(id) {
        $('<iframe />', {
            "class": "ncm-player",
            "src": `//music.163.com/outchain/player?type=2&id=${id}&auto=0&height=66`,
            'width': '330',
            'height': '86',
            'marginwidth': '0',
            'marginheight': '0'
        }).appendTo(this.messageContainer);
    }

    get empty() {
        return this.messageContainer.children.length == 0;
    }

    get container() {
        if (this.messageContainer.children().length == 0) {
            return null;
        }
        let q = $('<div class="mdui-container message" />');
        if (this.headerContainer.children().length) {
            this.headerContainer.appendTo(q);
        }
        this.messageContainer.appendTo(q);
        return q;
    }
}

class Sender {
    #username = document.getElementById('input-username').value;
    #nickname = document.getElementById('input-nickname').value;
    #avatar = document.getElementById('input-useravatar').value;
    #title = document.getElementById('input-usertitle').value;
    #title_style = document.getElementById('input-usertitle_style').value;

    constructor() { }

    get data() {
        return {
            username: this.#username,
            nickname: this.#nickname,
            avatar: this.#avatar,
            title: this.#title,
            title_style: this.#title_style
        }
    }
}

if (location.port) {
    path = `${location.hostname}:${location.port}/`;
}
else {
    path = `${location.hostname}/`;
}

var socket = new WebSocket(`ws://${path}`);
var sender = new Sender();
var lastSender = null;
var loading = false;

socket.onmessage = function (event) {
    var _ = JSON.parse(event.data);
    var type = _.type;
    var data = _.data;

    if (type == 'info') {
        if (data == 'history.begin') {
            loading = true;
        }
        if (data == 'history.end') {
            $('.status-indicator-ready').toggleClass('mdui-hidden');
            $('.status-indicator-loading').toggleClass('mdui-hidden');
            loading = false;
        }
    }
    else if (type == 'notice') {
        lastSender = null;
        $(`<div class="notice">${data}</div>`).appendTo('.message-container');
    }
    else if (type == 'message') {
        msg = new Message();
        if (data.sender && data.sender.username != lastSender) {
            msg.setSender(data.sender);
            lastSender = data.sender.username;
        }
        data.message.forEach(i => {
            if (i.type == 'text') {
                msg.appendText(i.data, i.attr)
            }
            else if (i.type == 'mention') {
                msg.appendMention(i.data);
            }
            else if (i.type == 'image') {
                msg.appendImage(i.data);
            }
            else if (i.type == 'ncm') {
                msg.appendNCM(i.data);
            }
        });

        if (msg.empty) return;

        msg.container.appendTo('.message-container');
    }

    if (document.getElementById('autoscroll-checkbox').checked) {
        var elem = document.querySelector('.message-container');
        if (loading) {
            elem.scroll({
                top: elem.scrollHeight,
                behavior: 'instant'
            });
        }
        else {
            elem.scroll({
                top: elem.scrollHeight,
                behavior: 'smooth'
            });
        }
    }
}

$('.editor').keydown(e => {
    if (e.key == 'Enter' && e.ctrlKey) {
        document.getElementById('send-button').click();
    }
});

socket.onopen = function (event) {
    socket.send(JSON.stringify({
        "type": "init",
        "data": {
            "sender": sender.data
        }
    }));
}

socket.onclose = function (event) {
    $('.status-indicator-ready').toggleClass('mdui-hidden');
    $('.status-indicator-fail').toggleClass('mdui-hidden');
    quill.disable();
}

function send() {
    let delta = quill.getContents();
    msg = [];
    if (delta.ops.length == 1 && delta.ops[0].insert.trim().length == 0) {
        mdui.snackbar('消息不能为空');
        return;
    }
    delta.ops.forEach(x => {
        if (x.insert.image) {
            if (!validateImage(x.insert.image)) {
                mdui.snackbar('Unrecognized image');
                return;
            }
            msg.push({
                'type': 'image',
                'data': x.insert.image
            });
        }
        else if (x.insert.mention) {
            msg.push({
                'type': 'mention',
                'data': x.insert.mention
            });
        }
        else if (x.insert.ncm) {
            msg.push({
                'type': 'ncm',
                'data': x.insert.ncm
            });
        }
        else if (typeof x.insert == 'string') {
            msg.push({
                'type': 'text',
                'data': x.insert,
                'attr': x.attributes
            });
        }
    });
    socket.send(JSON.stringify({
        "type": "message",
        "data": {
            "sender": sender.data,
            "message": msg
        }
    }));
    quill.deleteText(0, quill.getLength());
}
