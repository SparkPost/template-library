<a href="https://www.sparkpost.com"><img src="https://www.sparkpost.com/sites/default/files/attachments/SparkPost_Logo_2-Color_Gray-Orange_RGB.svg" width="200px"/></a>

[Sign up](https://app.sparkpost.com/join?src=Dev-Website&sfdcid=70160000000pqBb) for a SparkPost account and visit our [Developer Hub](https://developers.sparkpost.com) for even more content.

# SparkPost Email Template Library

This repository contains a selection of prebuilt email templates designed for use with SparkPost. Some, like the [features template](templates/features/) are meant to showcase SparkPost's personalisation capabilities. Others are starting points for your own email. For example, [here's a simple responsive template](templates/responsive/).

Each template is available as HTML, text and sample substitution data. You can also import a Postman collection containing all templates as SparkPost REST API requests.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/d2f3d0149a306779aa1e)

# Regenerating The Postman Collection

To automatically create a Postman collection from the template files:

```bash
python tools/buildPostmanCollection.py
```

# Contributing

Transparency is one of our core values, and we encourage developers to contribute and become part of the SparkPost developer community.

## Contribution Steps

1. Fork this repository
2. Create a new branch named after the issue you'll be addressing. Include the issue number as the branch name. For example: a branch named "ISSUE-8" would address issue number 8.
3. Make your changes, adding new templates or updating existing ones as necessary.
4. Remember to [regenerate the Postman collection](#regenerating-the-postman-collection) to include your changes.
5. Submit a new pull request applying your branch to the develop branch of this repository.

