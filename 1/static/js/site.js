/**
 * User: tianjie
 * Date: 13-4-22
 * Time: 下午10:52
 */
var siteTool = {
     log : function(msg, type, delay){
        delay = delay|| 2000;
        var _type = '';
        if(type === 'success')
            _type='alert-success';
        else if(type === 'info')
            _type = 'alert-info';
        else if(type === 'error')
            _type = 'alert-error';
        
        _type = _type || 'info'

        var _alert = $('<div class="alert '+ _type +' fade in" style=" position: fixed;right: 2%; bottom:1%"/>')
            .append('<button type="button" class="close" data-dismiss="alert">&times;</button>')
            .append(msg);
        $("body").prepend(_alert);
        _alert.show();
        window.setTimeout(function() {
            if(!_alert.is(":hidden"))
                _alert.alert('close')
        }, delay);
    },
    /**
     * 复选框的事件
     * @param selector 复选框的选择器
     * @param container 所有需要被选中或取消选中的复选框
     */
     bindCheckAllEvt : function(selector,container){
        $(selector).click(function(){
            var stats = $(this).attr('checked') || false;
            $(container).each(function(idx,item){
                $(item).attr('checked',stats);
            });
        });
        
        $(container).click(function(){
        	var chklen = $(container).filter(function(idx,el){
        		if($(el).attr('checked')){
        			return el;
        		}
        	}).length
			var chkStats = $(container).length === chklen;
    		$(selector).attr('checked',chkStats)
        });
    }
};