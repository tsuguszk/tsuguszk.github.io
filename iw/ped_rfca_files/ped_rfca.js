// Created by iWeb 3.0.4 local-build-20150514

function createMediaStream_id2()
{return IWCreatePhotocast("http://tsugu.private.coocan.jp/iw/ped_rfca_files/rss.xml",true);}
function initializeMediaStream_id2()
{createMediaStream_id2().load('http://tsugu.private.coocan.jp/iw',function(imageStream)
{var entryCount=imageStream.length;var headerView=widgets['widget0'];headerView.setPreferenceForKey(imageStream.length,'entryCount');NotificationCenter.postNotification(new IWNotification('SetPage','id2',{pageIndex:0}));});}
function layoutMediaGrid_id2(range)
{createMediaStream_id2().load('http://tsugu.private.coocan.jp/iw',function(imageStream)
{if(range==null)
{range=new IWRange(0,imageStream.length);}
IWLayoutPhotoGrid('id2',new IWPhotoGridLayout(2,new IWSize(295,295),new IWSize(295,112),new IWSize(306,422),27,27,0,new IWSize(18,31)),new IWPhotoFrame([IWCreateImage('ped_rfca_files/Pushpin_01.jpg'),IWCreateImage('ped_rfca_files/Pushpin_02.jpg'),IWCreateImage('ped_rfca_files/Pushpin_03.jpg'),IWCreateImage('ped_rfca_files/Pushpin_06.jpg'),IWCreateImage('ped_rfca_files/Pushpin_09.jpg'),IWCreateImage('ped_rfca_files/Pushpin_02_1.jpg'),IWCreateImage('ped_rfca_files/Pushpin_03_1.jpg'),IWCreateImage('ped_rfca_files/Pushpin_04.jpg')],null,1,0.500000,0.000000,0.000000,0.000000,0.000000,18.000000,18.000000,18.000000,18.000000,298.000000,472.000000,298.000000,472.000000,'ped_rfca_files/bullet_pp_3.png',new IWPoint(0.500000,-10),new IWSize(45,65),0.100000),imageStream,range,null,null,1.000000,{backgroundColor:'rgb(0, 0, 0)',reflectionHeight:100,reflectionOffset:2,captionHeight:100,fullScreen:0,transitionIndex:2},'Media/slideshow.html','widget0','widget1','widget2')});}
function relayoutMediaGrid_id2(notification)
{var userInfo=notification.userInfo();var range=userInfo['range'];layoutMediaGrid_id2(range);}
function onStubPage()
{var args=window.location.href.toQueryParams();parent.IWMediaStreamPhotoPageSetMediaStream(createMediaStream_id2(),args.id);}
if(window.stubPage)
{onStubPage();}
setTransparentGifURL('Media/transparent.gif');function applyEffects()
{var registry=IWCreateEffectRegistry();registry.registerEffects({stroke_0:new IWEmptyStroke()});registry.applyEffects();}
function hostedOnDM()
{return false;}
function onPageLoad()
{IWRegisterNamedImage('comment overlay','Media/Photo-Overlay-Comment.png')
IWRegisterNamedImage('movie overlay','Media/Photo-Overlay-Movie.png')
loadMozillaCSS('ped_rfca_files/ped_rfcaMoz.css')
adjustLineHeightIfTooBig('id1');adjustFontSizeIfTooBig('id1');NotificationCenter.addObserver(null,relayoutMediaGrid_id2,'RangeChanged','id2')
adjustLineHeightIfTooBig('id3');adjustFontSizeIfTooBig('id3');adjustLineHeightIfTooBig('id4');adjustFontSizeIfTooBig('id4');Widget.onload();fixupAllIEPNGBGs();fixAllIEPNGs('Media/transparent.gif');applyEffects()
initializeMediaStream_id2()}
function onPageUnload()
{Widget.onunload();}
