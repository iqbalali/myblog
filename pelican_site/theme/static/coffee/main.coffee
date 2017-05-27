# @codekit-prepend "../js/jquery-1.10.1.min.js", "../tipuesearch/tipuesearch_set.js", "../tipuesearch/tipuesearch.js", "../js/react.min.js", "../js/bigfoot.min.js";

d = React.DOM

React.initializeTouchEvents(true)

shuffle = (source) ->
  return source unless source.length >= 2

  for index in [source.length-1..1]
    randomIndex = Math.floor Math.random() * (index + 1)
    [source[index], source[randomIndex]] = [source[randomIndex], source[index]]
  source

Post = React.createFactory React.createClass
  getInitialState: ->
    trackingCampaign =
      pk_campaign: 'Top-Posts'
      pk_kwd: @props.post.title?.toLowerCase()
    trackingCampaignParams: @serialize trackingCampaign

  serialize: (obj) ->
    str = []
    for p of obj
      if obj.hasOwnProperty(p)
        str.push encodeURIComponent(p) + '=' + encodeURIComponent(obj[p])
    str.join '&'

  trackEvent: (title) ->
    if window.location.pathname.match(/\d{4}\/\d{2}\/\d{2}/)
      # This is a blog post
      _paq.push ['trackEvent', 'Top Posts', 'Article', title]
    else
      _paq.push ['trackEvent', 'Top Posts', 'Index', title]

  render: ->
    d.li {},
      d.span {},
        d.a {
          href: "#{@props.post.url}" # ?#{@state.trackingCampaignParams}
          onClick: => @trackEvent @props.post.title
          onTouchEnd: => @trackEvent @props.post.title
        }, @props.post.title

TopPosts = React.createClass
  getInitialState: ->
    dataUrl: '/json/top_articles.json'
    articles: []

  componentDidMount: ->
    $.get @state.dataUrl, (result) =>
      if @isMounted
        @setState articles: shuffle(result.articles)

  render: ->
    d.div {id: "container"},
      d.header {}, "Popular Posts this Month"
      d.ul {},
        @state.articles.map (article) -> Post post: article

RelatedPosts = React.createClass
  getInitialState: ->
    dataUrl: '/json/related_articles.json'
    articles: []

  componentDidMount: ->
    $.get @state.dataUrl, (result) =>
      if @isMounted
        @setState articles: shuffle(result.data[@props.slug])

  render: ->
    d.div {id: "container"},
      d.header {}, "Related Articles"
      d.ul {},
        @state.articles.map (article) -> Post post: article


MapCategories = React.createClass
  getInitialState: ->
    map._currentMarkers = []
    foodShow: false

  food: ->
    map.setView([51.505, -0.09], 7);
    markers = [
      L.marker([51.5, -0.09]).bindPopup('test1')
      L.marker([51.6, -0.09]).bindPopup('test2')
      L.marker([51.7, -0.09]).bindPopup('test3')
    ]
    window.markers = markers
    if not @state.foodShow
      for marker in markers
        marker.addTo(map)
        map._currentMarkers.push marker

    else
      for marker in map._currentMarkers
        map.removeLayer(marker)

    @setState foodShow: !@state.foodShow

  render: ->
      d.ul {},
          d.li {onClick: @food}, "Food"


$ ->
    $.bigfoot {
        preventPageScroll: false
    }
    top_posts = document.getElementById('top-posts')
    related_posts = document.getElementById('related-posts')

    slug = $('#slug').text()
    if top_posts
      React.render React.createElement(TopPosts, null, null), top_posts
    else if (related_posts and slug)
      React.render React.createElement(RelatedPosts, {slug: slug}, null), related_posts

    if window.location.pathname == "/pages/search.html"
      $('#tipue_search_input').tipuesearch();
      _paq.push(['trackSiteSearch',
          # Search keyword searched for
          tipue_search_query.toLowerCase(),
          # Search category selected in your search engine. If you do not need this, set to false
          false,
          # Number of results on the Search results page. Zero indicates a 'No Result Search Keyword'. Set to false if you don't know
          tipue_search_results_count
      ]);

    map_categories = document.getElementById('map_categories')
    if map_categories
      React.render React.createElement(MapCategories, null, null), map_categories
