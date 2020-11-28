import React, { useEffect, useState } from 'react'
import { useIntl } from 'react-intl'
import Page from 'material-ui-shell/lib/containers/Page'
import Scrollbar from 'material-ui-shell/lib/components/Scrollbar'
import ReactMarkdown from 'react-markdown'
import 'github-markdown-css'

export default function () {
  const [source, setSource] = useState(null)
  const intl = useIntl()

  const loadData = async () => {
    const text = '# Twitter-Search-Engine \nSearch Engine for Tweets - Project for Course Big Data Algorithms CMPE297'
    setSource(text)
  }

  useEffect(() => {
    loadData()
  }, [])

  return (
    <Page
      pageTitle={intl.formatMessage({ id: 'about', defaultMessage: 'About' })}
    >
      <Scrollbar>
        <div style={{ backgroundColor: 'white', padding: 12 }}>
          {source && (
            <ReactMarkdown
              className="markdown-body"
              source={source}
              escapeHtml
            />
          )}
        </div>
      </Scrollbar>
    </Page>
  )
}
