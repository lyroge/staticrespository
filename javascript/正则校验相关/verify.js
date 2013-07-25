/**
 * 通用js验证类
 * by 废墟
 * http://anerg.com
 */
var Validator = {
	label:{
		'username':'帐号',
		'password':'密码',
		'passconf':'密码确认',
		'email':'Email',
		'vcode':'验证码',
		'author':'笔名',
		'truename':'真实姓名',
		'qq':'QQ',
		'idcard':'身份证号码',
		'tel':'电话',
		'zipcode':'邮编',
		'address':'联系地址'
	},
	trim:function(item) {
		this.Value = $.trim(this.Value);
		item.val(this.Value);
	},
	require:function(item) {
		if(this.Value == '') {
			this.ErrorMessage[item.attr('name')] = '这是必填项，麻烦您啦^_^';
			return false;
		} else {
			return true;
		}
	},
	min_length:function(item, len) {
		if(this.getStrActualLen(this.Value) < len) {
			this.ErrorMessage[item.attr('name')] = '太短啦。必须超过'+len+'个字符';
			return false;
		} else {
			return true;
		}
	},
	max_length:function(item, len) {
		if(this.getStrActualLen(this.Value) > len) {
			this.ErrorMessage[item.attr('name')] = '太长啦。不能超过'+len+'个字符';
			return false;
		} else {
			return true;
		}
	},
	matches:function(item, filed) {
		var v = item.parents('form').find("input[name='"+filed+"']:visible").val();
		if(v != this.Value) {
			this.ErrorMessage[item.attr('name')] = '两次输入的'+this.label[filed]+'不一致 :(';
			return false;
		} else {
			return true;
		}
	},
	email:function(item) {
		var re = /^([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
		if(!re.test(this.Value)) {
			this.ErrorMessage[item.attr('name')] = "格式不正确呀，请检查一下";
			return false;
		} else {
			return true;
		}
	},
	qq:function(item) {
		var re = /^[0-9]{5,11}$/;
		if(!re.test(this.Value)) {
			this.ErrorMessage[item.attr('name')] = "格式不正确呀，请检查一下";
			return false;
		} else {
			return true;
		}
	},
	vcode:function(item) {
		var re = /^\d{4}$/;
		if(!re.test(this.Value)) {
			this.ErrorMessage[item.attr('name')] = "验证码错误";
			return false;
		} else {
			return true;
		}
	},
	idcard:function(item) {
		var re = /^(\d{15}$|^\d{18}$|^\d{17}(\d|X|x))$/;
		if(!re.test(this.Value)) {
			this.ErrorMessage[item.attr('name')] = "格式不正确呀，请检查一下";
			return false;
		} else {
			return true;
		}
	},
	checkusername:function(item) {
		var re = /^([\u4E00-\uFA29]|[\uE7C7-\uE7F3]|[a-zA-Z0-9])*$/;
		if(!re.test(this.Value)) {
			this.ErrorMessage[item.attr('name')] = "用户名只能包含中英文和数字";
			return false;
		} else {
			var _stat = true;
			var _this = this;
			$.ajax({
				async:false,
				type:'POST',
				url:'/ajax/checkusername',
				data:"username="+this.Value,
				dataType:'text',
				success:function(rs) {
					if(rs == 1) {
						_this.ErrorMessage[item.attr('name')] = '呃，已经被别人用了';
						_stat = false;
					} else if(rs == 9) {
						_this.ErrorMessage[item.attr('name')] = '换一个吧。Sorry :(';
						_stat = false;
					} else {
						_stat = true;
					}
				}
			});
			return _stat;
		}
		
	},
	userexists:function(item) {
		var _stat = true;
		var _this = this;
		$.ajax({
			async:false,
			type:'POST',
			url:'/ajax/checkusername',
			data:"username="+this.Value,
			dataType:'text',
			success:function(rs) {
				if(rs == 1 || rs == 9) {
					_stat = true;
				} else {
					_this.ErrorMessage[item.attr('name')] = '帐号不存在';
					_stat = false;
				}
			}
		});
		return _stat;
	},
	checkauthor:function(item) {
		var _stat = true;
		var _this = this;
		$.ajax({
			async:false,
			type:'POST',
			url:'/ajax/checkauthor',
			data:"author="+this.Value,
			dataType:'text',
			success:function(rs) {
				if(rs == 1) {
					_this.ErrorMessage[item.attr('name')] = '呃，已经被别人用了';
					_stat = false;
				} else if(rs == 9) {
					_this.ErrorMessage[item.attr('name')] = '换一个吧。Sorry :(';
					_stat = false;
				} else {
					_stat = true;
				}
			}
		});
		return _stat;
	},
	Items:[],
	ErrorMessage:[],
	Value:'',
	Validate:function(theItem) {
		if(typeof(theItem) != 'undefined') {
			this.Items = [];
			this.ErrorMessage = [];
			var valid = theItem.attr('valid');
			if(typeof(valid) != 'undefined') {
				this.Items[theItem.attr('name')] = theItem;
				this.Value = theItem.val();
				var method = valid.split('|');
				for(var i in method) {
					var re = /(.*)\[(.*[^\]])\]$/;
					if(re.test(method[i])) {
						var tmp = method[i].match(re);
						if(typeof(this[tmp[1]]) == 'function' && this[tmp[1]](theItem, tmp[2]) == false)
							break;
					} else {
						if(typeof(this[method[i]]) == 'function' && this[method[i]](theItem) == false)
							break;
					}
				}
				
				show_rs(this.Items, this.ErrorMessage);
				
				if(this.count(this.ErrorMessage) > 0) {
					return false;
				} else {
					return true;
				}
			}
		}
	},
	count:function(obj) {
		var counter = 0;
		for(i in obj) counter++;
		return counter;
	},
	getStrActualLen:function(sChars){
		sChars = $.trim(sChars);
		var len = 0;
		for(i=0;i<sChars.length;i++){
			iCode = sChars.charCodeAt(i);
			if((iCode>=0 && iCode<=255)||(iCode>=0xff61 && iCode<=0xff9f)){
				len += 1;
			}else{
				len += 2;
			}
		}
		return len;
	}
}