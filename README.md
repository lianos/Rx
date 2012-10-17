Rx: Take two and call me in the morning
=======================================

This is a package currently under development for [Sublime Text 2][st2] that
enhances its functionality as an editor for the [R language][rlang].

Included functionality:

  * Adds syntax file to support editing [Rmarkdown][rmd].

  * Enhanced "send command to R process" functionality (from [R tools][rtools])
    that allows you to send R commands to an R process from any section of a
    document that is scoped as R code (`source.r.*`). This allows you to send
    code within chunks of [SWeave][sweave] and [knitr][knitr] documents.

The impetus to develop this package was to support authoring Rmarkdown files in
something besides [Rstudio][rstudio]. While Rstudio is a great project, its
editor was too slow to work in for me *on my machine*, which left me pining for
something a bit less painful. I have been using [Emacs/ESS][ess] for the longest
time, but I know Python much better than elisp, and I've always felt a bit more
at home with [TextMate][tm]-like editors.

The initial functionality for sending commands to a running R process was
forked from the excellent [R tools package][rtools].

This code is released under the [Apache 2][apache2] license.

[apache2]: http://www.apache.org/licenses/LICENSE-2.0.html
[ess]: http://ess.r-project.org
[knitr]: http://yihui.name/knitr
[rlang]: http://www.r-project.org
[rmd]: http://rstudio.org/docs/authoring/using_markdown
[rstudio]: http://www.rstudio.org
[rtools]: https://github.com/karthikram/Rtools
[st2]: http://www.sublimetext.com
[sweave]: http://www.statistik.lmu.de/~leisch/Sweave
[tm]: http://macromates.com/
