// Copyright 2024 Notedown Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package cmd

import (
	"fmt"

	"github.com/notedownorg/library/pkg/html"
	"github.com/notedownorg/library/pkg/notedown"
	"github.com/notedownorg/notedown/pkg/providers/source"
	"github.com/spf13/cobra"
)

var articleCmd = &cobra.Command{
	Use:   "article <url>",
	Short: "Add a new article to your library",
	Long:  `Add the metadata of an article to your library for post-processing to asynchronously fill in the rest.`,
	Args:  cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		cfg, url := loadConfig(), args[0]

		title, err := html.ExtractTitle(url)
		if err != nil {
			return fmt.Errorf("failed to extract title: %w", err)
		}

		client, err := notedown.NewClient(cfg.root)
		if err != nil {
			return fmt.Errorf("failed to create notedown client: %w", err)
		}

		if err := client.CreateSource(client.NewSourceLocation(title), title, source.Article, url); err != nil {
			return fmt.Errorf("failed to create source: %w", err)
		}

		return nil
	},
}

func init() {
	addCmd.AddCommand(articleCmd)
}
